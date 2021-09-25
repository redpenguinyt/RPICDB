import discord, random, asyncpraw, os
from discord.ext import commands
from discord_slash import cog_ext

reddit = asyncpraw.Reddit(
    client_id=os.environ['reddit_id'],
    client_secret=os.environ['reddit_secret'],
    user_agent=os.environ['reddit_user_agent'],
)

class Suggested(commands.Cog):
	"""General commands"""

	def __init__(self, bot):
		self.bot = bot
	
	@cog_ext.cog_subcommand(
		base="suggested",
        name="wheretohidetoxicwaste",
        description="Where to hide toxic waste")
	async def wheretohidetoxicwaste(self, ctx):
		randomx = random.randint(-160,160)
		randomy = random.randint(-160,160)
		where = f"https://www.google.com/maps/@{randomx},{randomy},10z"
		await ctx.send(
			embed=discord.Embed(color=0xe74c3c,
			title=f"Here: {where}")
		)
	
	@cog_ext.cog_subcommand(
		base="suggested",
        name="randomquestion",
        description="Get a random question")
	async def randomquestion(self, ctx):
		await ctx.defer()
		subreddit = await reddit.subreddit("AskReddit", fetch=True)
		question = await subreddit.random()
		await ctx.send(
			embed=discord.Embed(
				color=0xe74c3c,
				title=question.title,
			)
		)
	
	@cog_ext.cog_subcommand(
		base="suggested",
        name="ppsize",
        description="Check a user's pp size")
	async def ppsize(self, ctx, user: discord.Member):
		if not user:
			user = ctx.message.author
		embed = discord.Embed(
			title = f"{user.name}\'s pp:",
			description=f"8{'=' * random.randint(0,10)}D"
		)
		await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Suggested(bot))