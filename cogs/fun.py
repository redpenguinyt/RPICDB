import discord, os, random, asyncpraw, requests, json
from discord.ext import commands
from utils import prettysend
from discord import app_commands

reddit = asyncpraw.Reddit(
    client_id=os.environ['reddit_id'],
    client_secret=os.environ['reddit_secret'],
    user_agent=os.environ['reddit_user_agent'],
)

async def find_meme(ctx, subreddit):
	try:
		requestedsub = await reddit.subreddit(subreddit) # , fetch=True
	except:
		await ctx.response.send_message("Could not find that subreddit")
		return 1

	post = await requestedsub.random()
	i = 0
	while not post or post.is_self or post.url.startswith("https://v."):
		i += 1
		if i > 10:
			await ctx.response.send_message("Could not find an image post on that subreddit")
			return 1
		post = await requestedsub.random()
	
	if post.over_18:
		if not ctx.channel.is_nsfw():
			await ctx.response.send_message("The bot tried to send an nsfw command in a non-nsfw channel! If this was a mistake, run the command again")
			return 1

	return post

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

rickrollmsgs = [
	"I found this cool thing %s",
	"Yo check this out %s",
	"Cute video of doggo :3 %s",
	"Adorable cat video %s"
]

rickrolllinks = [
	"https://www.youtube.com/watch?v=QB7ACr7pUuE",
	"https://www.youtube.com/watch?v=-51AfyMqnpI",
	"https://www.youtube.com/watch?v=SWk1X0buyxQ",
	"https://www.youtube.com/watch?v=2942BB1JXFk",
]

def get_quote():  # get a random quote
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

class Fun(commands.Cog):
	""" Fun! FUn! FUN! """

	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="8ball", description="Shake that 8ball for wisdom!")
	async def eightball(self, ctx, question: str):
		result = random.choice(eightball)
		await prettysend(ctx, f"{ctx.user} asked \"{question}\"", result)

	@app_commands.command(description="poop")
	async def poop(self, ctx):
		await ctx.response.send_message(
			embed=discord.Embed(color=0xe74c3c,
			title="Poop", 
			description = poopascii
			)
		)

	@app_commands.command(description="Post a meme!")
	async def meme(self, ctx, subreddit:str="memes"):
		await ctx.response.defer(thinking=True)

		meme = await find_meme(ctx, subreddit)

		if meme == 1:
			return

		embed = discord.Embed(title=meme.title,color=0xe74c3c)
		embed.set_image(url=meme.url)
		embed.set_footer(text=f"Credit to u/{meme.author.name}")
		await ctx.followup.send(embed=embed)
	
	@app_commands.command(description='Rickroll!')
	async def rickroll(self, ctx):
		embed = discord.Embed(
			title='Rickroll posted',
			color=0xe74c3c
		)
		embed.set_thumbnail(url='https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif')

		rickroll = random.choice(rickrollmsgs) % f"<{random.choice(rickrolllinks)}>"
		await ctx.channel.send(rickroll)
		await ctx.response.send_message(embed=embed, ephemeral=True)
		
	@app_commands.command(description="Reverse whatever you say!")
	async def reverse(self, ctx, message: str):
		await prettysend(ctx, message[::-1])

	@app_commands.command(description="Get an inspiring quote!")
	async def inspire(self, ctx):
		await prettysend(ctx, get_quote())

	@app_commands.command(description="Compliment someone!")
	async def compliment(self, ctx, target:discord.Member):
		await prettysend(ctx, "", random.choice(compliments) % target.mention)
	
	@app_commands.command(description="RPICDB will help you choose something!")
	async def choose(self, ctx, choice1:str, choice2:str, choice3:str="", choice4:str="", choice5:str=""):
		choices = [choice1,choice2,choice3,choice4,choice5]
		for choice in choices:
			if choice == "":
				choices.pop(choices.index(choice))
		await prettysend(ctx, random.choice(choices))
	
	@app_commands.command(description="Roll the dice!")
	async def dice(self, ctx):
		await prettysend(ctx,
			"Dice", str(random.randint(1,6))
		)

async def setup(bot):
	await bot.add_cog(Fun(bot))