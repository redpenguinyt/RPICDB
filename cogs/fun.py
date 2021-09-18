import discord, os, random, asyncpraw, requests, json
from discord.ext import commands
from utils import getinfofromguild, prettysend
from discord_slash import cog_ext

reddit = asyncpraw.Reddit(
    client_id=os.environ['reddit_id'],
    client_secret=os.environ['reddit_secret'],
    user_agent=os.environ['reddit_user_agent'],
)

compliments = [  # List of encouragements
    "%s is amazing!",
	"Round of applause for %s",
	"You are a great person, %s",
    "%s's mum iz gae",
    "%s, I'm proud of you",
    "your hair is nice %s"
]

eightball = [ # list of 8ball answers
	"100% no",
	"not rly",
	"lol no",
	"maybe",
	"kinda",
	"hecc yeah",
	"of course"
]

poopascii = """
░░░░░░░░░░░█▀▀░░█░░░░░░
░░░░░░▄▀▀▀▀░░░░░█▄▄░░░░
░░░░░░█░█░░░░░░░░░░▐░░░
░░░░░░▐▐░░░░░░░░░▄░▐░░░
░░░░░░█░░░░░░░░▄▀▀░▐░░░
░░░░▄▀░░░░░░░░▐░▄▄▀░░░░
░░▄▀░░░▐░░░░░█▄▀░▐░░░░░
░░█░░░▐░░░░░░░░▄░█░░░░░
░░░█▄░░▀▄░░░░▄▀▐░█░░░░░
░░░█▐▀▀▀░▀▀▀▀░░▐░█░░░░░
░░▐█▐▄░░▀░░░░░░▐░█▄▄░░
░░░▀▀░▄POOP▄░░░▐▄▄▄▀░░░
"""

def get_quote():  # get a random quote
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

class Fun(commands.Cog):
	""" Fun! FUn! FUN! """

	def __init__(self, bot):
		self.bot = bot

	@cog_ext.cog_slash(name="8ball", description="Shake that 8ball for wisdom!")
	async def eightball(self, ctx, question):
		await prettysend(ctx, question, random.choice(eightball))

	@cog_ext.cog_slash(description="poop")
	async def poop(self, ctx):
		await ctx.send(
			embed=discord.Embed(color=0xe74c3c,
			title="Poop", 
			description = poopascii
			)
		)

	@cog_ext.cog_slash(description="Post a meme!")
	async def meme(self, ctx, subreddit="memes"):
		await ctx.defer()
		try:
			if not getinfofromguild(ctx.guild.id, "premium") and subreddit != "memes":
				subreddit = "memes"
				await ctx.send("Custom subreddits require premium! In the meantime, enjoy a meme from r/memes",hidden=True)
		except: subreddit = "memes"
		requestedsub = None
		try:
			requestedsub = await reddit.subreddit(subreddit, fetch=True)
		except:
			await ctx.send("Could not find that subreddit, sorry!",hidden=True)
			return
		
		post = await requestedsub.random()
		
		embed = discord.Embed(title=post.title,color=0xe74c3c)
		embed.set_image(url=post.url)
		embed.set_footer(text=f"Credit to u/{post.author.name}")
		await ctx.send(embed=embed)
	
	@cog_ext.cog_slash(description='Rickroll!')
	async def rickroll(self, ctx):
		embed = discord.Embed(
			title='Rickroll',
			description='Never gonna give you up',
			color=0xe74c3c
		)
		embed.set_image(url='https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif')
		embed.add_field(name='Click here', value='[Click Here!](https://youtube.com/watch?v=dQw4w9WgXcQ/)')

		await ctx.send(embed=embed)
		
	@cog_ext.cog_slash(description="Reverse whatever you say!")
	async def reverse(self, ctx, *, message):
		await prettysend(ctx, message[::-1])

	@cog_ext.cog_slash(description="Get an inspiring quote!")
	async def inspire(self, ctx):
		await prettysend(ctx, get_quote())

	@cog_ext.cog_slash(description="Compliment someone!")
	async def compliment(self, ctx, target: discord.Member):
		await prettysend(ctx, "", random.choice(compliments) % target.mention)
	
	@cog_ext.cog_slash(description="RPICDB will help you choose something!")
	async def choose(self, ctx, choice1, choice2, choice3="", choice4="", choice5=""):
		choices = [choice1,choice2,choice3,choice4,choice5]
		for choice in choices:
			if choice == "":
				choices.pop(choices.index(choice))
		await prettysend(ctx, random.choice(choices))
	
	@cog_ext.cog_slash(description="Roll the dice!")
	async def dice(self, ctx):
		await prettysend(ctx, "Dice", random.randint(1,6))

def setup(bot):
	bot.add_cog(Fun(bot))