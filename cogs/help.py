import discord
from discord.ext import commands
import json
import asyncio


def get_prefix(id):
 try:
   with open('prefix.json', "r") as f:
     prefix = json.load(f)
   prefixes = prefix[str(id)]
 except:
   prefixes = "-"
 return prefixes

class Fun(commands.Cog):
 def __init__(self, client):
   self.client = client


 @commands.Cog.listener()
 async def on_ready(self):
   pass


 @commands.command()
 async def help(self, ctx):
   prefix = get_prefix(ctx.guild.id)
   embed = discord.Embed(color = discord.Colour.blue())
   embed.title = 'Help Menu'
   embed.description = f'Use these commands for more help menus\n{prefix}**help <category>**'
   embed.add_field(name='Fun',value=':smile: | `Fun Commands!`')
   embed.add_field(name='Info',value=':page_facing_up: | `Info Commands!`',inline=False)
   embed.add_field(name='Mod',value=':shield: | `Moderation Commands!`',inline=False)

   msg = await ctx.send(embed=embed)
   emojis = ["😄", "📄", "🛡️"]
   categories = ['Fun', 'Info', 'Mod']

   for helprec in emojis:
     await msg.add_reaction(helprec)

   loopNotClosed = True

   def check(reaction, user):
     return user == ctx.message.author and str(reaction.emoji) in emojis

   while loopNotClosed:
     try:
       reaction, user = await self.client.wait_for('reaction_add', timeout=3600.0, check=check)
       await msg.remove_reaction(reaction.emoji, ctx.message.author)

       category = categories[emojis.index(reaction.emoji)]

       helpEmbed = discord.Embed(
         title=f"{category} Commands",
         color=discord.Color.blue()
       )

       for cmd in self.client.commands:
         if cmd.brief == category:
           helpEmbed.add_field(name=cmd.name, value=f"{prefix}{cmd.name} {cmd.help}", inline=False)

       await msg.edit(content=" ", embed = helpEmbed)

     except asyncio.TimeoutError:
       await msg.clear_reactions()
       loopNotClosed = False


def setup(client):
 client.add_cog(Fun(client))