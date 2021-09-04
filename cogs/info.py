import discord
from discord.ext import commands
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Info(commands.Cog):
 def __init__(self, client):
   self.client = client


 @commands.Cog.listener()
 async def on_ready(self):
   pass


# User Info
 @commands.command(aliases=['userinfo','whois'], brief='Info', help='<user>')
 async def user(self, ctx, user:discord.Member=None):
   if user == None:
     user = ctx.author

   userAge = relativedelta(datetime.utcnow(),user.created_at)
   userAge = f'`{userAge.years} Years {userAge.months} Months {userAge.days} Days {userAge.hours}h {userAge.minutes}m {userAge.seconds}s`'
   
   customActivity = ''.join([str(a.name) for a in user.activities if a.type is discord.ActivityType.custom])

   if customActivity == '':
     customActivity = 'None'
   
   userRoles = None
   userTopRole = None
   if len(user.roles) > 1:
     userRoles = ', '.join(role.mention for role in user.roles[1:])
     userTopRole = user.top_role.mention

   userStatus = user.status
   if userStatus == discord.Status.dnd:
     userStatus = 'Do Not Disturb'
   
   userPlatform = ['Unknown']
   if user.desktop_status != discord.Status.offline:
     userPlatform.append('Computer')
   if user.web_status != discord.Status.offline:
     userPlatform.append('Web')
   if user.mobile_status != discord.Status.offline or user.is_on_mobile():
     userPlatform.append('Mobile')
   if len(userPlatform) > 1:
     userPlatform = userPlatform[1:]
   userPlatform = ', '.join(userPlatform)


   embed = discord.Embed(color = discord.Colour.blue())
   
   embed.set_thumbnail(url=user.avatar_url)
   embed.add_field(name='Identification',value=f'Mention: {user.mention}\nServer Nickname: `{user.display_name}`\nTag: `{user}`\nID: `{user.id}`')
   embed.add_field(name='-',value=f'Is A Bot: `{user.bot}`')
   embed.add_field(name='Discord Account',value=f'Account Age: {userAge}\nJoined On: `{user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")}`\nCreated On: `{user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")}`\nStatus: `{userStatus}`\nCustom Activity: `{customActivity}`\nPlatforms Online: `{userPlatform}`',inline=False)
   embed.add_field(name='Roles',value=userRoles)
   embed.add_field(name='Highest Role',value=userTopRole)
   embed.add_field(name='Permissions',value=', '.join([perm[0] for perm in user.guild_permissions if perm[1]]),inline=False)
   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • User Info • UTC Time")
   await ctx.send(embed=embed)


# Server Info
 @commands.command(aliases=['serverinfo'], brief='Info', help='')
 async def server(self, ctx):
   if not ctx.guild:
     return

   serverAge = relativedelta(datetime.utcnow(),ctx.guild.created_at)
   serverAge = f'`{serverAge.years} Years {serverAge.months} Months {serverAge.days} Days {serverAge.hours}h {serverAge.minutes}m {serverAge.seconds}s`'

   textChannels = len(ctx.guild.text_channels)
   vcChannels = len(ctx.guild.voice_channels)
   allChannels = textChannels + vcChannels

   embed = discord.Embed(
     title = ctx.guild.name,
     color = discord.Colour.blue()
   )
   embed.set_thumbnail(url=ctx.guild.icon_url)
   embed.add_field(name='Identification',value=f'Name: `{ctx.guild.name}`\nOwner: {ctx.guild.owner.mention}\nID: `{ctx.guild.id}`',inline=False)
   embed.add_field(name='Age',value=f'Server Age: `{serverAge}`\nCreated On: `{ctx.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")}`',inline=False)
   embed.add_field(name='Members',value=f'All Users: `{ctx.guild.member_count}`\nHumans: `{len(list(filter(lambda b: not b.bot, ctx.guild.members)))}`\nBots: `{len(list(filter(lambda b: b.bot, ctx.guild.members)))}`')
   embed.add_field(name='Channels',value=f'All Channels: `{allChannels}`\nChannels: `{textChannels}`\nVoice Channels: `{vcChannels}`')
   embed.add_field(name='Roles',value=f'Number of Roles: `{len(ctx.guild.roles)}`',inline=False)
   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • Server Info • UTC Time")
   await ctx.send(embed=embed)


# Bot Info
 @commands.command(aliases=['botinfo'], brief='Info', help='')
 async def bot(self, ctx):
   embed = discord.Embed(
     title = self.client.user.name,
     color = discord.Colour.blue()
   )
   embed.add_field(name='Info',value=f'Developer: `Danny_#9755`\nVersion: `Alpha 0.5`\nAPI: `Discord.py {discord.__version__}`\nPing: `{round(self.client.latency*1000,1)}ms`')
   embed.add_field(name='Description',value='```I\'m a fast and powerful bot that is under heavy developement! I cover a lot of things such as moderation, server information, fun games, and so much more! Did I mention that all my commands are 100% FREE!!```',inline=False)
   embed.add_field(name='Invite Link',value='There is currently no invite link since the bot is undergoing alpha : (',inline=False)
   embed.set_thumbnail(url=self.client.user.avatar_url)
   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • Bot Info • UTC Time")
   await ctx.send(embed=embed)

def setup(client):
 client.add_cog(Info(client))