import discord
from discord.ext import commands
import json
import os
from discord_slash import SlashCommand


def getPrefix(client, message):
 with open('prefix.json','r') as f:
   prefixes = json.load(f)
 try:
   return prefixes[str(message.guild.id)]
 except:
   return '-'

client = commands.Bot(command_prefix=getPrefix,intents=discord.Intents().all(),help_command=None, case_insensitive=True)
slash = SlashCommand(client, sync_commands=True)

for filename in os.listdir('./cogs'):
 if filename.endswith('.py'):
   client.load_extension(f'cogs.{filename[:-3]}')
   print("Loaded", filename)


# @client.command()
# async def load(ctx, extension):
#  client.load_extension(f'cogs.{extension}')

# @client.command()
# async def unload(ctx, extension):
#  client.unload_extension(f'cogs.{extension}')


@client.event
async def on_ready():
 await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="For -help"))
 print('-' * 20)
 print(client.user.name, "is online")
 print("ID:", client.user.id)
 print('-' * 20)


client.run(os.getenv("TOKEN"))