import discord, os, random, asyncpraw, requests, json
from discord.ext import commands
from utils import getinfofromguild, prettysend

reddit = asyncpraw.Reddit(
    client_id=os.environ['reddit_id'],
    client_secret=os.environ['reddit_secret'],
    user_agent=os.environ['reddit_user_agent'],
)

hapwrds = [  # List of encouragements
    "%s is amazing!",
	"Round of applause for %s",
	"You are a great person, %s",
    "%s's mum iz gae",
    "%s, I'm proud of you",
    "your hair is nice %s"
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

	@commands.command(help="poop")
	async def poop(self, ctx):
		await ctx.send("""
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
		""")

	@commands.command(help="post a meme!")
	async def meme(self, ctx, sub="memes"):
		sub.replace("r/","")
		if not getinfofromguild(ctx.guild.id, "premium") and sub != "memes":
			sub = "memes"
			await ctx.reply("Custom subreddits require premium! In the meantime, enjoy a meme from r/memes")
		subreddit = await reddit.subreddit(sub, fetch=True)
		if subreddit.over18:
			ctx.reply("BONK no horny")
			return
		meme = await subreddit.random()
		if meme.over_18:
			await meme(self, ctx, sub)
			return
		embed = discord.Embed(title=meme.title,color=0xe74c3c)
		embed.set_image(url=meme.url)
		embed.set_footer(text=f"Credit to u/{meme.author.name}")
		await ctx.send(embed=embed)
	
	@commands.command(help='Rickroll!')
	async def rickroll(self, ctx):
		embed = discord.Embed(title='Rickroll',description='Never gonna give you up',color=0xe74c3c)
		embed.set_author(name=ctx.author.name,url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',icon_url=ctx.author.avatar_url)
		embed.set_image(url='https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif')

		embed.add_field(name='Click here', value='[Click Here!](https://youtube.com/watch?v=dQw4w9WgXcQ/)')
		embed.set_footer(text='Made in Python', icon_url='http://i.imgur.com/5BFecvA.png')

		await ctx.send(embed=embed)
		
	@commands.command(help="reverse whatever you say!", aliases=["r"])
	async def reverse(self, ctx, *, message):
		await prettysend(ctx, message[::-1])

	@commands.command(brief="inspiring quote!")
	async def inspire(self, ctx):
		await prettysend(ctx, get_quote())

	@commands.command(help="compliment someone!", aliases=["c"])
	async def compliment(self, ctx, target):
		await ctx.send(random.choice(hapwrds) % target)
	
	@commands.command(help="RPICDB will help you choose something!")
	async def choose(self, ctx, *, things="yes no"):
		await prettysend(ctx, random.choice(things.split(" ")))

def setup(bot):
	bot.add_cog(Fun(bot))