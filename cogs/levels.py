import discord, json, random
from discord.ext import commands
from utils import config
from replit import db

config = config()

def update_data(user: discord.User):
	if not f"{user.id}" in db["users"]:
		print("hi")
		db["users"][f"{user.id}"] = {"xp":0,"level":1}


def add_xp(user: discord.User, exp):
	db["users"][f"{user.id}"]['xp'] += exp


async def level_up(user: discord.User, msg):
	xp = db["users"][f"{user.id}"]['xp']
	lvl = db["users"][f"{user.id}"]['level']
	lvl_lmt = lvl * config["lvlmultiplier"]
	if xp >= lvl_lmt:
		await msg.channel.send(f'{user.mention} has leveled up to level {lvl + 1}')
		db["users"][f"{user.id}"]['level'] = lvl + 1
		db["users"][f"{user.id}"]['xp'] = xp - lvl_lmt
class Levels(commands.Cog):
	"""Levels"""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		update_data(member)


	@commands.Cog.listener()
	async def on_message(self, msg):
		guild = msg.channel.guild
		guilds = json.load(open('data/guilds.json', 'r'))
		isLevels = True
		if f"{guild.id}" in guilds:
			isLevels = guilds[f"{guild.id}"]["isLevels"]
		if not msg.author.bot and isLevels:
			update_data(msg.author)
			add_xp(msg.author, random.randint(3,8))
			await level_up(msg.author, msg)

		await self.bot.process_commands(msg)
	
	@commands.command(help="Give XP to a user")
	@commands.has_permissions(manage_messages=True)
	async def givexp(self, ctx, amount=100, user: discord.User=None):
		if not user:
			user = ctx.message.author

		update_data(user)
		add_xp(user, amount)
		await level_up(user, ctx)

		await ctx.reply(f"Gave {amount} XP to {user.mention}")

def setup(bot):
    bot.add_cog(Levels(bot))