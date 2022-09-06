import discord, random, asyncpraw, os
from discord.ext import commands
from discord import app_commands

reddit = asyncpraw.Reddit(
    client_id=os.environ['reddit_id'],
    client_secret=os.environ['reddit_secret'],
    user_agent=os.environ['reddit_user_agent'],
)

class Suggested(commands.GroupCog, name="suggested"):
	"""General commands"""

	def __init__(self, bot):
		self.bot = bot
	
	@app_commands.command(
        name="wheretohidetoxicwaste",
        description="Where to hide toxic waste")
	async def wheretohidetoxicwaste(self, ctx):
		randomx = random.randint(-160,160)
		randomy = random.randint(-160,160)
		where = f"https://www.google.com/maps/@{randomx},{randomy},10z"
		await ctx.response.send_message(
			embed=discord.Embed(color=0xe74c3c,
			title=f"Here: {where}")
		)
	
	@app_commands.command(
        name="randomquestion",
        description="Get a random question")
	async def randomquestion(self, ctx):
		await ctx.response.defer(thinking=True)
		subreddit = await reddit.subreddit("AskReddit", fetch=True)
		question = await subreddit.random()
		while question.over_18:
			question = await subreddit.random()
		await ctx.followup.send(f"> {question.title}")
	
	@app_commands.command(
        name="pickupline",
        description="Get a random pickup line")
	async def pickupline(self, ctx):
		await ctx.response.defer(thinking=True)
		subreddit = await reddit.subreddit("pickuplines", fetch=True)
		pickupline = await subreddit.random()
		while pickupline.over_18:
			pickupline = await subreddit.random()
		tosend = f"> {pickupline.title}"
		if pickupline.selftext:
			tosend += f"\n {pickupline.selftext}"
		await ctx.followup.send(tosend)

	@app_commands.command(
        name="ppsize",
        description="Check a user's pp size")
	async def ppsize(self, ctx, user: discord.Member):
		if not user:
			user = ctx.message.author
		embed = discord.Embed(
			title = f"{user.name}\'s pp:",
			description=f"8{'=' * random.randint(1,10)}D"
		)
		await ctx.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Suggested(bot))