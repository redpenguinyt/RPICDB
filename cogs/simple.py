import discord, json, requests, random
from discord.ext import commands

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

class Simple(commands.Cog):
	"""Example commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="test the bot's connection")
	async def test(self,ctx):
		await ctx.reply("I'm connected! :D", delete_after=3.0)

	@commands.command(help="Invite a user")
	async def invite(self, ctx, user: discord.User):
		await ctx.reply("Invite sent!", delete_after=3.0)
		invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
		await user.send("You have been invited to " + str(invitelink))

	@commands.command(help="reverse whatever you say!")
	async def reverse(self, ctx, *, message):
		await ctx.reply(message[::-1], delete_after=3.0)

	@commands.command(brief="inspiring quote!")
	async def inspire(self, ctx):
		await ctx.reply(get_quote(), delete_after=3.0)

	@commands.command(help="compliment someone!")
	async def compliment(self, ctx, target):
		await ctx.channel.send(random.choice(hapwrds) % target)

def setup(bot):
    bot.add_cog(Simple(bot))