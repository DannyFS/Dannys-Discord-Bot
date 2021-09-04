import discord
from discord.ext import commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from termcolor import colored as color


def get_prefix(id):
 try:
   with open('prefix.json', 'r') as f:
     prefix = json.load(f)
   prefixes = prefix[str(id)]
 except:
   prefixes = "-"
 return prefixes


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


class Events(commands.Cog):
 def __init__(self, client):
   self.client = client


 @commands.Cog.listener()
 async def on_ready(self):
   pass


 @commands.Cog.listener()
 async def on_command_completion(self, ctx):
   print(color(f"Successfully executed command", "green") + str(": " + ctx.command.name))


#  @commands.Cog.listener()
#  async def on_error(event, *args, **kwargs):
#    print("FUCK")


#  @commands.Cog.listener()
#  async def on_command_error(self, ctx, error):
#    print(color(error, "red"))

#    embed = discord.Embed(
#      title = 'An Unexpected Error Occurred!!',
#      description = f"```diff\n- {error}```",
#      color = discord.Color.red()
#    )

#    await ctx.send(embed=embed)


 @commands.Cog.listener()
 async def on_message(self, message):
   if message.author.bot:
     return

   if message.guild:
     print(f'({color(message.guild.id, "blue")}, {color(message.author.id, "blue")}) {color(message.author, "cyan")}: {message.content}')

     with open('guildinfo.json', 'r') as f:
       log = json.load(f)
     guildID = str(message.guild.id)

     if guildID in log:
       guildShit = log[guildID]
       if "counting" in guildShit:
         channelID = guildShit["counting"]

         if message.channel.id == channelID:
           channel = discord.utils.get(message.guild.channels, id = channelID)
           pastMessage = await channel.history(limit=2).flatten()
           pastMessage = pastMessage[1]
           print(pastMessage.content)

           if int(pastMessage.content) + 1 != int(message.content):
             await message.delete()
             await message.channel.send("Opps! You can only send a leading number in this channel!", delete_after=5)


   if message.content == "<@!614176993419853824>":
     embed = discord.Embed(color = discord.Color.blue())
     if message.guild:
       prefix = get_prefix(message.guild.id)
       embed.description = f'Prefix for {message.guild.name} is `{prefix}`\n**Use {prefix}help for more info**'
     else:
       embed.description = f'Hi there! I am {self.client.user.name}!\nIf you are having trouble, type `-help`'
     await message.channel.send(embed=embed)


 @commands.Cog.listener()
 async def on_message_delete(self, message):
   user = message.author
   await sendToLogs(message, message.guild, 'Message Deleted', f'**Message sent by {user.mention} deleted in {message.channel.mention}\n[Jump to message]({message.jump_url})**\n{message.content}', f'Author ID: {user.id} • Message ID: {message.id}', user, discord.Color.red())


 @commands.Cog.listener()
 async def on_message_edit(self, before, after):
   user = after.author

   if not before.pinned and after.pinned:
     await sendToLogs(None, after.guild, 'Message Pinned', f'**Message sent by {user.mention} pinned in {after.channel.mention}\n[Jump to message]({after.jump_url})**\n{after.content}', f'Author ID: {user.id} • Message ID: {after.id}', None, discord.Color.blue())
  

   elif before.pinned and not after.pinned:
     await sendToLogs(None, after.guild, 'Removed Pin Message', f'**Message sent by {user.mention} pinned in {after.channel.mention} was removed\n[Jump to message]({after.jump_url})**\n{after.content}', f'Author ID: {user.id} • Message ID: {after.id}', None, discord.Color.red())

   else:
     await sendToLogs(None, after.guild, 'Message Edited', f'**Message sent by {user.mention} edited in {after.channel.mention}\n[Jump to message]({after.jump_url})\nBefore:**\n{before.content}\n**After:**\n{after.content}', f'Author ID: {user.id} • Message ID: {after.id}', user, discord.Color.blue())


 @commands.Cog.listener()
 async def on_member_join(self, user):
   with open('guildinfo.json','r') as f:
     welcome = json.load(f)

   userAge = relativedelta(datetime.utcnow(),user.created_at)
   userAge = f'{userAge.years} Years {userAge.months} Months {userAge.days} Days {userAge.hours}h {userAge.minutes}m {userAge.seconds}s'

   await sendToLogs(None, user.guild, 'Member Joined Server', f'{user.mention} {user}\n**Account Age:** {userAge}', f'User ID: {user.id}', None, discord.Color.green(), user.avatar_url)

   embed = discord.Embed(title = f'*Welcome to {user.guild.name} Discord Server!*', color = discord.Color.green())

   embed.set_thumbnail(url = user.avatar_url)
   embed.set_footer(text = user.name, icon_url = user.avatar_url)

   guildID = str(user.guild.id)

   if guildID in welcome:
     if "welcome" in welcome[guildID]:
       welcomeShit = welcome[guildID]["welcome"]
       if welcomeShit[1] != "":
         embed.description = welcomeShit[1]
       else:
         embed.description = f'Welcome {user.mention} to the {user.guild.name} Discord Server! There is a total of {user.guild.member_count} members! Enjoy your stay!'
       await self.client.get_channel(welcomeShit[0]).send(embed=embed)


 @commands.Cog.listener()
 async def on_member_remove(self, user):
   await sendToLogs(None, user.guild, 'Member Left Server', f'{user.mention} {user}', f'User ID: {user.id}', None, discord.Color.red(), user.avatar_url)


#  @commads.Cog.listener()
#  async def on_member_update(self, before, after):
   

#  @commads.Cog.listener()
#  async def on_guild_update(before, after):


#  @commads.Cog.listener()
#  async def on_guild_role_create(role):


#  @commads.Cog.listener()
#  async def on_guild_role_delete(role):


#  @commads.Cog.listener()
#  async def on_guild_role_update(before, after):


 @commands.Cog.listener()
 async def on_guild_join(self, guild):
   with open('prefix.json','r') as f:
     prefixes = json.load(f)
   prefixes[str(guild.id)] = '-'
   with open('prefix.json','w') as f:
     json.dump(prefixes, f)

   await guild.create_role(name="Muted By Danny's Bot")
   
   print(color("Client joined a server:", "green"), f'{color(guild, "cyan")} ({color(guild.id, "blue")})')


 @commands.Cog.listener()
 async def on_guild_remove(self, guild):
   with open('prefix.json','r') as f:
     prefixes = json.load(f)
   prefixes.pop(str(guild.id))
   with open('prefix.json','w') as f:
     json.dump(prefixes, f)
  
   print(color("Client left a server:", "red"), f'{color(guild, "cyan")} ({color(guild.id, "blue")})')


def setup(client):
 client.add_cog(Events(client))