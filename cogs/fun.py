import discord, os, random
from discord.ext import commands
try:
	import asyncpraw
except:
	os.system("pip install asyncpraw")
	import asyncpraw


reddit = asyncpraw.Reddit(
    client_id="h1-03_17OBrD1A",
    client_secret=os.environ['reddit_secret'],
    user_agent="chrome-browser - RPICDB:v0.0.1 (by /u/RedPenguin_YT)",
)

class Fun(commands.Cog):
	""" Fun! FUn! FUN! """

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="post a meme!")
	async def meme(self, ctx, subreddit="memes"):
		subreddit = await reddit.subreddit(subreddit)
		if subreddit.over18:
			ctx.reply(f"@everyone {ctx.message.author.mention} is very horny")
			return
		meme = await subreddit.random()
		embed = discord.Embed(title=meme.title,color=0xe74c3c)
		embed.set_image(url=meme.url)
		embed.set_footer(text=f"Credit to u/{meme.author.name}")
		await ctx.channel.send(embed=embed)
	
	@commands.command(help="RPICDB will help you choose something! chooses yes or no by default")
	async def choose(self, ctx, *, things="yes no"):
		await ctx.reply(random.choice(things.split(" ")))

def setup(bot):
	bot.add_cog(Fun(bot))