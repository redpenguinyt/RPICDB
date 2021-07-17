import random, asyncpraw, os
from discord.ext import commands
from utils import prettysend

reddit = asyncpraw.Reddit(
    client_id=os.environ['reddit_id'],
    client_secret=os.environ['reddit_secret'],
    user_agent=os.environ['reddit_user_agent'],
)

class Suggested(commands.Cog):
	"""General commands"""

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(help="Where to hide toxic waste", aliases=["wthtw"])
	async def wheretohidetoxicwaste(self, ctx):
		randomx = random.randint(-160,160)
		randomy = random.randint(-160,160)
		where = f"https://www.google.com/maps/@{randomx},{randomy},10z"
		await prettysend(ctx, f"Here: {where}")
	
	@commands.command(help="Get a random question", aliases=["rq"])
	async def randomquestion(self, ctx):
		subreddit = await reddit.subreddit("AskReddit", fetch=True)
		question = await subreddit.random()
		if question.over_18:
			return
		await prettysend(ctx, question.title)

def setup(bot):
    bot.add_cog(Suggested(bot))