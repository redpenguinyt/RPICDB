import discord, random
from discord.ext import commands
from utils import config, load_json
from replit import db

config = config()

def update_data(user: discord.User):
	if not f"{user.id}" in db["users"]:
		db["users"][f"{user.id}"] = {"xp":0,"level":1}


def add_xp(user: discord.User, exp):
	db["users"][f"{user.id}"]['xp'] += exp


async def level_up(user: discord.User, msg):
	xp = db["users"][f"{user.id}"]['xp']
	lvl = db["users"][f"{user.id}"]['level']
	lvl_lmt = lvl * config["lvlmultiplier"]
	while xp >= lvl_lmt:
		db["users"][f"{user.id}"]['level'] = lvl + 1
		db["users"][f"{user.id}"]['xp'] = xp - lvl_lmt
		xp = xp - lvl_lmt
		lvl = lvl + 1
		lvl_lmt = lvl * config["lvlmultiplier"]
		await msg.channel.send(f"GG, {user.mention}! You\'ve leveled up to level {lvl + 1}")
class Levels(commands.Cog):
	"""Levels"""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		update_data(member)


	@commands.Cog.listener()
	async def on_message(self, msg):
		guild = msg.guild
		if not guild:
			return
		guilds = load_json("data/guilds.json")
		isLevels = True
		if f"{guild.id}" in guilds:
			isLevels = guilds[f"{guild.id}"]["isLevels"]
		if not msg.author.bot and isLevels:
			update_data(msg.author)
			add_xp(msg.author, random.randint(3,8))
			await level_up(msg.author, msg)
	
	@commands.command(help="Give XP to a user")
	@commands.is_owner()
	async def givexp(self, ctx, amount=100, user: discord.User=None):
		if not user:
			user = ctx.message.author

		update_data(user)
		add_xp(user, amount)
		await level_up(user, ctx)

		await ctx.reply(f"Gave {amount} XP to {user.mention}")
	
	@commands.command(help="Check the levelling leaderboard")
	@commands.guild_only()
	async def top(self, ctx):
		users = db["users"]
		topusers = sorted(users.items(), key= lambda x: (x[1]['level'], x[1]['xp']), reverse=True)[:5]
		tosend = "Top level members: \n"
		i = 0
		for user in topusers:
			try:
				name = ctx.guild.get_member(int(topusers[i][0]))
				level = topusers[i][1]['level']
				tosend += f"`{i+1}. {name} - Level {level}` \n"
			except:
				tosend += f"`{i+1}. No user found` \n"
			i += 1
		await ctx.send(tosend)

def setup(bot):
    bot.add_cog(Levels(bot))