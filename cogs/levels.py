import discord, json, random
from discord.ext import commands
from utils import config
from replit import db

config = config()

def update_data(users, user: discord.User):
	if not f'{user.id}' in users:
		users[f'{user.id}'] = {}
		users[f'{user.id}']['xp'] = 0
		users[f'{user.id}']['level'] = 1
	return users


def add_xp(users, user: discord.User, exp):
	users[f'{user.id}']['xp'] += exp
	return users


async def level_up(users, user: discord.User, msg):
	xp = users[f'{user.id}']['xp']
	lvl = users[f'{user.id}']['level']
	lvl_lmt = lvl * config["lvlmultiplier"]
	if xp >= lvl_lmt:
		await msg.channel.send(f'{user.mention} has leveled up to level {lvl + 1}')
		users[f'{user.id}']['level'] = lvl + 1
		users[f'{user.id}']['xp'] = xp - lvl_lmt
	return users

class Levels(commands.Cog):
	"""Levels"""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		users = json.load(open('data/users.json', 'r'))
		update_data(users, member)
		json.dump(users, open('data/users.json', 'w'), indent=4)


	@commands.Cog.listener()
	async def on_message(self, msg):
		guild = msg.channel.guild
		guilds = json.load(open('data/guilds.json', 'r'))
		isLevels = True
		if f"{guild.id}" in guilds:
			isLevels = guilds[f"{guild.id}"]["isLevels"]
		if not msg.author.bot and isLevels:
			users = json.load(open('data/users.json', 'r'))

			update_data(users, msg.author)
			add_xp(users, msg.author, random.randint(3,8))
			await level_up(users, msg.author, msg)

			json.dump(users, open('data/users.json', 'w'), indent=4)

		await self.bot.process_commands(msg)
	
	@commands.command(help="Give XP to a user")
	@commands.has_permissions()
	async def givexp(self, ctx, user: discord.User=None, amount=10):
		users = json.load(open('data/users.json', 'r'))
		if not user:
			user = ctx.message.author

		update_data(users, user)
		add_xp(users, user, amount)
		await level_up(users, user, ctx)

		json.dump(users, open('data/users.json', 'w'), indent=4)

def setup(bot):
    bot.add_cog(Levels(bot))