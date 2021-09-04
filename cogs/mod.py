import discord
from discord.ext import commands
import asyncio
import json
from datetime import datetime


def addModLog(userID, guildID, punishment, reason):
 with open('modlogs.json', 'r') as f:
   report = json.load(f)
 if not guildID in report:
   report[guildID] = {}
 if not userID in report[guildID]:
   report[guildID][userID] = []

 report[guildID][userID].append({
   'type': punishment,
   'reason': reason
 })

 with open('modlogs.json','w') as f:
   json.dump(report, f, sort_keys=True, ensure_ascii=False, indent=1, default=str)
   #json.dump(report, f, separators=(',', ':'))


def addToGuildInfo(guildID, key, value):
 with open('guildinfo.json','r') as f:
   guildInfo = json.load(f)
 guildInfo[guildID][key] = value
 with open('guildinfo.json','w') as f:
   json.dump(guildInfo, f, sort_keys=True, ensure_ascii=False, indent=1, default=str)


async def sendToLogs(message, guild: discord.Guild, title, description, footer, author: discord.User, color, thumbnail=None):
 with open('guildinfo.json', 'r') as f:
   log = json.load(f)
 guildID = str(guild.id)

 if not guildID in log:
   return
 
 if author:
   if author.id == 614176993419853824:
     return

 logChannel = discord.utils.get(guild.channels, id=log[guildID]["log"])

 if message:
   if message.channel == logChannel:
     return

 embed = discord.Embed(description=description, color=color, timestamp = datetime.utcnow())

 if title and not author:
   embed.title = title
 
 elif title and author:
   embed.set_author(name=title, icon_url=author.avatar_url)

 if thumbnail:
   embed.set_thumbnail(url=thumbnail)

 embed.set_footer(text=footer)

 await logChannel.send(embed=embed)


async def sendInfo(ctx, user, punishment, reason):
 embed = discord.Embed(title = f'You have been {punishment} on {ctx.guild.name}',color = discord.Colour.red())
 embed.add_field(name='Reason', value=reason)
 if not user.bot:
   try:
     await user.send(embed=embed)
   except:
     pass

 embed.title = f'Successfully {punishment} {user} ({user.id})'
 await ctx.send(embed=embed)


async def checkPerms(ctx, user):
 if (user.top_role >= ctx.author.top_role) or (user == ctx.author):
   embed = discord.Embed(title='**Permission denied**',color=discord.Colour.red())
   await ctx.send(embed=embed)
   return True
 return False


class Mod(commands.Cog):
 def __init__(self, client):
   self.client = client


 @commands.Cog.listener()
 async def on_ready(self):
   pass


 @commands.command(aliases=['clear'], brief='Mod', help='<number>')
 @commands.has_permissions(manage_messages=True)
 async def purge(self, ctx, amount=1):
   await ctx.channel.purge(limit = amount + 1)
 
 @purge.error # MAKE EMBED
 async def purge_error(self, ctx, error):
   if isinstance(error, commands.MissingRequiredArgument):
     await ctx.send("Proper syntax: `-purge <number>`")
   else:
     await ctx.send("Something bad happened : (")


 @commands.command(brief='Mod', help='<number><s/m/h>')
 @commands.has_permissions(manage_channels=True)
 async def slowmode(self, ctx, seconds='0'):
   embed = discord.Embed(color=discord.Colour.blue())
   if seconds[-1] in ['s','m','h']:
     timeConvert = {'s':1,'m':60,'h':3600}
     seconds = int(seconds[:-1]) * timeConvert[seconds[-1]]
   await ctx.channel.edit(slowmode_delay=int(seconds))
   embed.title = f'Successfully set the slowmode to {seconds}!'
   await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='<user>')
 @commands.has_permissions(manage_guild=True)
 async def modlogs(self, ctx, user:discord.User):
   userID = str(user.id)
   guildID = str(ctx.guild.id)
   with open('modlogs.json', 'r') as f:
     report = json.load(f)
   if not guildID in report:
     return await ctx.send("Ur server is spotless :D")
   if not userID in report[guildID]:
     return await ctx.send("This user is a very good person :D")
   
   embed = discord.Embed(
     title=f"{user} Mod Logs",
     color=discord.Colour.blue()
   )

   num = 1
   for modlog in report[guildID][userID]:
     embed.add_field(name=f'{num}. {modlog["type"]}', value=f'Reason: {modlog["reason"]}', inline=False)
     num += 1

   await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='<user> <log number>')
 @commands.has_permissions(manage_guild=True)
 async def removelog(self, ctx, user:discord.User, num:int):
   if not num:
     return
   
   userID = str(user.id)
   guildID = str(ctx.guild.id)

   with open('modlogs.json', 'r') as f:
     report = json.load(f)

   if not guildID in report:
     return await ctx.send("Ur server is spotless :D")
   if not userID in report[guildID]:
     return await ctx.send("This user is a very good person :D")

   del report[guildID][userID][num - 1]

   with open('modlogs.json','w') as f:
     json.dump(report, f, sort_keys=True, ensure_ascii=False, indent=1, default=str)

   embed = discord.Embed(
     title='Success!',
     description=f'I successfully cleared {user.mention} #{num} modlog',
     color=discord.Colour.green()
   )

   await ctx.send(embed=embed)



 @commands.command(brief='Mod', help='<user> <reason>')
 @commands.has_permissions(kick_members=True)
 async def warn(self, ctx, user:discord.Member, *, reason=None):
   if await checkPerms(ctx, user):
     return

   if reason:
     addModLog(str(user.id), str(ctx.guild.id), 'warn', reason)
     await sendInfo(ctx, user, 'warned', reason)
   else:
     embed = discord.Embed(title='Provide a reason!', description='Syntax: **-warn <user> <reason>**',color = discord.Colour.red())
     await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='<user> <number><s/m/h/d>')
 @commands.has_permissions(ban_members=True)
 async def mute(self, ctx, user:discord.Member, time='30m', *, reason='Sorry, we\'ve decided to temporarily mute you'):
   if await checkPerms(ctx, user):
     return

   addModLog(str(user.id), str(ctx.guild.id), 'mute', reason)

   time = time.lower()
   waitTime = 0
   if time[-1] in 'smhd':
     timeConvert = {'s':1,'m':60,'h':3600,'d':86400}
     waitTime = int(time[:-1]) * timeConvert[time[-1]]
   else:
     waitTime = int(time)
   role = discord.utils.get(ctx.guild.roles, name="Muted By Danny's Bot")
   await user.add_roles(role)
   embed = discord.Embed(title=f'You have been temporarily muted from {ctx.guild.name} for {time}',color = discord.Colour.red())
   embed.add_field(name='Reason',value=reason)
   await user.send(embed=embed)
   embed.title = f'Successfully muted {user} ({user.id}) for {time}'
   await ctx.send(embed=embed)
   await asyncio.sleep(waitTime)
   await user.remove_roles(role)

 @mute.error
 async def mute_error(self, ctx, error):
   embed = discord.Embed(color=discord.Colour.red())
   if isinstance(error, commands.MissingPermissions):
     embed.title = 'You don\'t have permission to run this command!'
   elif isinstance(error, commands.MissingRequiredArgument):
     embed.title = 'Who do you want to mute?'
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-mute <user> <time> <reason>**'
   else:
     embed.title = 'Something bad happened : ('
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-mute <user> <time> <reason>**'
   await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='<user> <reason>')
 @commands.has_permissions(kick_members=True)
 async def kick(self, ctx, user:discord.Member, *, reason='Sorry, we\'ve decided to kick you'):
   if await checkPerms(ctx, user):
     return
   await sendInfo(ctx, user, 'kicked', reason)
   await user.kick(reason=reason)
   addModLog(str(user.id), str(ctx.guild.id), 'kick', reason)
 
 @kick.error
 async def kick_error(self, ctx, error):
   embed = discord.Embed(color = discord.Colour.red())
   if isinstance(error, commands.MissingPermissions):
     embed.title = 'You don\'t have permission to run this command!'
   elif isinstance(error, commands.MissingRequiredArgument):
     embed.title = 'Who do you want to kick?'
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-kick <user> <reason>**'
   else:
     embed.title = 'Something bad happened : ('
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-kick <user> <reason>**'
   await ctx.send(embed=embed)


 @commands.command(aliases=['softban'], brief='Mod', help='<user> <number><s/m/h/d>')
 @commands.has_permissions(ban_members=True)
 async def tempban(self, ctx, user:discord.Member, time='7d', *, reason='Sorry, we\'ve decided to temporarily ban you'):
   if await checkPerms(ctx, user):
     return

   addModLog(str(user.id), str(ctx.guild.id), 'tempban', reason)

   waitTime = 0
   if time[-1] in 'smhd':
     timeConvert = {'s':1,'m':60,'h':3600,'d':86400}
     waitTime = int(time[:-1]) * timeConvert[time[-1]]
   else:
     waitTime = int(time)
   embed = discord.Embed(title=f'You have been temporarily banned from {ctx.guild.name} for {time}',color = discord.Colour.red())
   embed.add_field(name='Reason',value=reason)
   await user.send(embed=embed)
   await user.ban(reason=reason)
   embed.title = f'Successfully banned {user} ({user.id}) for {time}'
   await ctx.send(embed=embed)
   await asyncio.sleep(waitTime)
   await ctx.guild.unban(user)

 @tempban.error
 async def tempban_error(self, ctx, error):
   embed = discord.Embed(color=discord.Colour.red())
   if isinstance(error, commands.MissingPermissions):
     embed.title = 'You don\'t have permission to run this command!'
   elif isinstance(error, commands.MissingRequiredArgument):
     embed.title = 'Who do you want to temp ban?'
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-tempban <user> <time> <reason>**'
   else:
     embed.title = 'Something bad happened : ('
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-tempban <user> <time> <reason>**'
   await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='<user> <reason>')
 @commands.has_permissions(ban_members=True)
 async def ban(self, ctx, user:discord.Member, *, reason='Sorry, we\'ve decided to ban you'):
   if await checkPerms(ctx, user):
     return

   await sendInfo(ctx, user, 'banned', reason)
   await user.ban(reason=reason)
   addModLog(str(user.id), str(ctx.guild.id), 'ban', reason)
 
 @ban.error
 async def ban_error(self, ctx, error):
   embed = discord.Embed(color=discord.Colour.red())
   if isinstance(error, commands.MissingPermissions):
     embed.title = 'You don\'t have permission to run this command!'
   elif isinstance(error, commands.MissingRequiredArgument):
     embed.title = 'Who do you want to ban?'
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-ban <user> <reason>**'
   else:
     embed.title = 'Something bad happened : ('
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-ban <user> <reason>**'
   await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='<user id>')
 @commands.has_permissions(ban_members=True)
 async def unban(self, ctx, userID:int):
   bannedUsers = await ctx.guild.bans()
   for banEntry in bannedUsers:
     user = banEntry.user
     if userID == user.id:
       await ctx.guild.unban(user)
       embed = discord.Embed(title=f'Successfully unbanned {user} ({userID})',color = discord.Colour.red())
       return await ctx.send(embed=embed)

 @unban.error
 async def unban_error(self, ctx, error):
   embed = discord.Embed(color=discord.Colour.red())
   if isinstance(error, commands.MissingPermissions):
     embed.title = 'You don\'t have permission to run this command!'
   elif isinstance(error, commands.MissingRequiredArgument):
     embed.title = 'Who do you want to unban?'
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-unban <user> <reason>**'
   else:
     embed.title = 'Something bad happened : ('
     embed.description = 'Please provide an ID!\nSyntax: **-ban <user> <reason>**'
   await ctx.send(embed=embed)


  # HACKBAN:
 @commands.command(brief='Mod', help='<user id> <reason>', description="Ban a user outside of the server by ID!")
 @commands.has_permissions(ban_members=True)
 async def hackban(self, ctx, userID: int, *, reason=None):
   author = ctx.message.author
   server = author.guild
  
   user = server.get_member(userID)
   if user:
     return await ctx.invoke(self.ban, user=user)

   await self.client.http.ban(userID, server.id, 0)
   embed = discord.Embed(title=f'Successfully unbanned {user} ({userID})',color = discord.Colour.red())
   await ctx.send(embed=embed)
   return


 @hackban.error
 async def hackban_error(self, ctx, error):
   embed = discord.Embed(color=discord.Colour.red())
   if isinstance(error, commands.MissingPermissions):
     embed.title = 'You don\'t have permission to run this command!'
   elif isinstance(error, commands.MissingRequiredArgument):
     embed.title = 'Who do you want to unban?'
     embed.description = 'Mention a user or provide an ID!\nSyntax: **-hackban <user> <reason>**'
   else:
     embed.title = 'Something bad happened : ('
     embed.description = 'Please provide an ID!\nSyntax: **-hackban <user> <reason>**'
   await ctx.send(embed=embed)


 @commands.command(brief='Mod', help='prefix <prefix>\n-set welcome <channel>')
 @commands.has_permissions(administrator=True)
 async def set(self, ctx, choice='', *, details:str=None):
   choice = choice.lower()
   message = ctx.message
   embed = discord.Embed(color=discord.Colour.blue())

   if choice == '':
     embed.title = 'Command Types:'
     embed.description = 'Use these categories\n-set <category>'
     embed.add_field(name='Prefix',value='`Sets the prefix for this bot`')
   
   elif choice in ['counting', 'log']:
     channels = message.channel_mentions
     if not channels:
       return

     addToGuildInfo(str(ctx.guild.id), choice, channels[0].id)

   elif choice == 'prefix':
     if not ' ' in details:
       with open('prefix.json','r') as f:
         prefixes = json.load(f)
       prefixes[str(ctx.guild.id)] = details
       with open('prefix.json','w') as f:
         json.dump(prefixes, f)
      #  await ctx.guild.me.edit(nick=f'Dannys Bot [{details}]')
       embed.title = 'Success!'
       embed.description = f'I successfully set the prefix to **{details}**'

     else:
       embed.title = 'Invalid Prefix!'
       embed.description = 'My prefix cannot have a space!\n-set prefix <prefix>'


   elif choice == 'welcome':
     channels = message.channel_mentions
     if not channels:
       return

     channel = channels[0]
     details = details.replace(channel.mention, "").strip()

     addToGuildInfo(str(ctx.guild.id), 'welcome', [channel.id, details])

   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • Set Command")
   await ctx.send(embed=embed)


def setup(client):
 client.add_cog(Mod(client))