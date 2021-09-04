import discord
from discord.ext import commands
import random
from PyDictionary import PyDictionary
import requests
import datetime
import aiohttp
import json


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


#  @commands.command(brief='Fun', aliases=['ttt'])
#  async def tictactoe(self, ctx, player2: discord.Member = None):
#    if not player2:
#      return

#    player1 = ctx.author
   
#    embed = discord.Embed(title='Tic Tac Toe', description = ":white_large_square::white_large_square::white_large_square:\n:white_large_square::white_large_square::white_large_square:\n:white_large_square::white_large_square::white_large_square:", color=discord.Color.blue())

#    await ctx.send(embed=embed)


 @commands.command(name='8ball', brief='Fun', help='<question>', description='Lets you see the future')
 async def _8ball(self, ctx, *, question):
   responces = ['As I see it, yes','Ask again later','Better not tell you now','Cannot predict now','Concentrate and ask again','Don’t count on it','It is certain','It is decidedly so','Most likely','My reply is no','My sources say no','Outlook not so good','Outlook good','Reply hazy, try again','Signs point to yes','Very doubtful','Without a doubt','Yes','Yes – definitely','You may rely on it']
   embed = discord.Embed(title='THE MAGICAL 8 BALL',color=discord.Color.blue())
   embed.add_field(name='Question',value=question)
   embed.add_field(name='Answer',value=random.choice(responces),inline=False)
   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • 8 Ball")
   await ctx.send(embed=embed)

 @_8ball.error
 async def _8ball_error(self, ctx, error):
   embed = discord.Embed(color=discord.Colour.red())
   if isinstance(error, commands.MissingRequiredArgument):
     embed.title = "What is you're question?"
     embed.description = 'Provide a question!\nSyntax: **-8ball <quetion>**'
   else:
     embed.title = 'Something bad happened : ('
   await ctx.send(embed=embed)


 @commands.command(brief='Fun', help='', description='Sends a random image of a cat')
 async def cat(self, ctx):
   data = requests.get('https://aws.random.cat/meow').json()
   embed = discord.Embed(
     title = 'Heres a random kitty cat:',
     color = discord.Colour.blue()
   )
   embed.set_image(url=data['file'])            
   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • Cat")
   await ctx.send(embed=embed)


 @commands.command(brief='Fun', help='', description='Flips a coin')
 async def coinflip(self, ctx):
   embed = discord.Embed(title='Coin Flip',color=discord.Color.blue())
   embed.add_field(name='Result:',value=f"`{random.choice(['Heads','Tails'])}`")
   embed.set_thumbnail(url='attachment://coin.png')
   await ctx.send(file=discord.File("pics/coin.png",filename="coin.png"),embed=embed)


 @commands.command(aliases=['dadjokes'], help='', brief='Fun', description='Sends a random dad joke')
 async def dadjoke(self, ctx):
   joke = random.choice(open('textfiles/dadjokes.txt').read().splitlines())
   if '~' in joke:
     joke = joke.replace('~','\n')
   await ctx.send(f'{ctx.author.mention}\n{joke}')


 @commands.command(brief='Fun', help='<word>', description='Looks up a definition of a word')
 async def dictionary(self, ctx, *, word=''):
   embed = discord.Embed()
   dictWord = PyDictionary().meaning(word)
   if dictWord != None and word != '':
     embed.title = word
     embed.color = discord.Color.blue()
     items = dictWord.items()
     for meaning in items:
       embed.add_field(name=meaning[0],value=meaning[1][0],inline=False)
   else:
     embed.title = 'Unknown Word!'
     embed.description = 'Make sure the spelling is correct!\nSyntax: **-dictionary <word>**'
     embed.color = discord.Color.red()
   
   await ctx.send(embed=embed)


 @commands.command(brief='Fun', help='', description='Sends a random image of a dog')
 async def dog(self, ctx):
   data = requests.get('https://dog.ceo/api/breeds/image/random').json()
   embed = discord.Embed(
     title = 'Heres a random dog:',
     color = discord.Colour.blue()
   )
   embed.set_image(url=data['message'])            
   embed.set_footer(icon_url=self.client.user.avatar_url,text="Danny's Bot • Dog")
   await ctx.send(embed=embed)


 @commands.command(aliases=['murder'], brief='Fun', help='<user>', description='Lets you kill anyone in the server')
 async def kill(self, ctx, user:discord.Member=None):
   murder = []
   if user == None:
     murder = [f'{random.choice(["You couldnt find anyone to kill!","A murder plan is not a good murder plan without a victim!", "You had some dark thoughts..."])}\nNext time use:\n**-kill <user>**']
   elif user == ctx.author:
     murder = ['You blew yourself up','You shot your head while looking at the inside of the gun\'s barrel','You tried toasting bread in a bath tub','You fell while mountain climbing without a harness!',f'You were eaten by a{random.choice([" shark","n allegator"," tiger"," lion"," jet engine"])}']
   elif user == self.client.user:
     murder = [f'{random.choice(["Haha nice try, you cant kill me!","How dare you try to kill me!","I thought we were friends : ("])}\n*Gets gun\nShoots {ctx.author.mention}*','Im calling the police!',f'Hey! I was planning to kill you\n*Kidnapps {ctx.author.mention}*']
   else:
     murder = [f'{ctx.author.mention} killed {user.mention} with a {random.choice(["gun","knife","cooking pan","deep fryer","football","golf club","car","train","school bus","pill","bomb"])}!', f'{ctx.author.mention} pushed {user.mention} down the stairs!', f'{ctx.author.mention} shot {user.mention} with a {random.choice(["pistol","shotgun","water gun","cannon","tank"])}']
   await ctx.send(random.choice(murder))


 @commands.command(brief='Fun', help='', description='Shows latency')
 async def ping(self, ctx):
   embed = discord.Embed(title='Pong!',color=discord.Color.blue())
   embed.add_field(name='The latency is',value=f"`{round(self.client.latency*1000,1)}ms`")
   embed.set_thumbnail(url='attachment://paddle.png')
   await ctx.send(file=discord.File("pics/paddle.png",filename="paddle.png"),embed=embed)


 @commands.command(brief='Fun', help='<city>', description='Lets the bot say a phrase')
 async def weather(self, ctx, *, varos):
   try:
     complete_url = "http://api.openweathermap.org/data/2.5/weather?appid=b27c7c507ef7da3a9235a0f93318beca&q=" + varos
     async with aiohttp.ClientSession() as session:
       async with session.get(complete_url) as r:
         x = await r.json()
         if x["cod"] != "404":
           import pytemperature
           y = x["main"]
           z = x["weather"]
           t = x["sys"]
           w = x["wind"]
           current_temperature = y["temp"]
           embed = discord.Embed(title=f'Weather information for {varos.title()}, {t["country"]}', description = z[0]["description"],color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
           embed.add_field(name="**Temperature**", value=f"{int(pytemperature.k2c(current_temperature))}°C/{int(pytemperature.k2f(current_temperature))}°F")
           embed.add_field(name="**Humidity**", value=f'{y["humidity"]}%')
           embed.add_field(name="**Wind**", value=f'{w["speed"]}mph at {w["deg"]}°')
           embed.set_footer(icon_url=self.client.user.avatar_url,text="Weather")
           await ctx.send(embed=embed)
         else:
           await ctx.send(":x: Cannot find this **city**!")
   except Exception:
     await ctx.send(f":x: Couldn't retrieve data for {varos}!")


 @commands.command(brief='Fun', help='', description='Sends a random yo mama joke')
 async def yomama(self, ctx):
   joke = random.choice(open('textfiles/yomama.txt').read().splitlines())
   if '~' in joke:
     joke = joke.replace('~','\n')
   await ctx.send(f'{ctx.author.mention}\n{joke}')


def setup(client):
 client.add_cog(Fun(client))