import discord
from discord.ext import commands
import praw
import random


reddit = praw.Reddit(
 client_id = "CLIENT ID",
 client_secret = "SECRET",
 user_agent = "AGENT",
 username = "USER",
 password = "PASS",
)

def fillList(subreddit):
 subreddit = reddit.subreddit(subreddit)
 redditList = []

 for submission in subreddit.hot(limit=1000):
   image = submission.url
 
   if "https://i.redd.it/" in image:
     redditList.append(image)
 return redditList


async def sendImage(ctx, post):
 embed = discord.Embed(color = discord.Color.blue())
 embed.set_image(url = post)

 await ctx.send(embed = embed)


class Reddit(commands.Cog):
 def __init__(self, client):
   self.client = client
   self.memes = fillList("memes")


 @commands.Cog.listener()
 async def on_ready(self):
   pass


 @commands.command()
 async def meme(self, ctx):
   post = random.choice(self.memes)
   await sendImage(ctx, post)


 @commands.command()
 async def reddit(self, ctx, subreddit):
   post = ''
   subreddit = reddit.subreddit(subreddit)
   for submission in subreddit.hot(limit=1):
     image = submission.url
 
     if "https://i.redd.it/" in image:
       post = image
   await ctx.send(post)


def setup(client):
 client.add_cog(Reddit(client))