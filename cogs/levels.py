import discord, random
from discord.ext import commands
from utils import config, prettysend, getinfofromguild
from replit import db
from discord_slash import cog_ext

config = config()

def update_data(user: discord.Member):
	if not f"{user.guild.id}" in db["guilds"]:
		db["guilds"][f"{user.guild.id}"] = config["defaultguild"]
	if not f"{user.id}" in db["guilds"][f"{user.guild.id}"]["users"]:
		db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"] = {"xp":0,"level":1}

def add_xp(user: discord.Member, exp):
	db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"]['xp'] += exp

def remove_xp(user: discord.Member, exp):
	db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"]["xp"] -= exp

async def level_up(user: discord.Member, ctx):
	xp = db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"]['xp']
	lvl = db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"]['level']
	old_lvl = lvl
	lvl_lmt = lvl * config["lvlmultiplier"]
	while xp >= lvl_lmt:
		db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"]['level'] = lvl + 1
		db["guilds"][f"{user.guild.id}"]["users"][f"{user.id}"]['xp'] = xp - lvl_lmt
		xp = xp - lvl_lmt
		lvl = lvl + 1
		lvl_lmt = lvl * config["lvlmultiplier"]
	if lvl != old_lvl:
		embed = discord.Embed(
			title = "Level Up!",
			description = f"GG, {user.mention}! You\'ve leveled up to level {lvl}",
			color=0xe74c3c
		)
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.channel.send(embed=embed)
		
	
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
		isLevels = True
		isLevels = getinfofromguild(msg.guild.id, "isLevels")
		if not msg.author.bot and isLevels:
			update_data(msg.author)
			add_xp(msg.author, random.randint(3,8))
			await level_up(msg.author, msg)
	
	@cog_ext.cog_subcommand(
		base="exp",
        name="give",
        description="Give XP to a user")
	async def givexp(self, ctx, amount: int, user: discord.Member=None):
		if not ctx.author.guild_permissions.manage_messages:
			ctx.send("You don't have the right permissions ;-;", hidden=True)
			return
		if not user:
			user = ctx.author

		update_data(user)
		add_xp(user, amount)
		await level_up(user, ctx)

		await ctx.send(f"Gave {amount} XP to {user.mention}",hidden=True)
	
	@cog_ext.cog_subcommand(
		base="exp",
        name="remove",
        description="Take XP from a user")
	async def takexp(self, ctx, amount: int, user: discord.Member=None):
		if not ctx.author.guild_permissions.manage_messages:
			ctx.send("You don't have the right permissions ;-;", hidden=True)
			return
		if not user:
			user = ctx.author

		update_data(user)
		remove_xp(user, amount)
		await level_up(user, ctx)

		await ctx.reply(f"Took {amount} XP from {user.mention}")

	@cog_ext.cog_subcommand(
		base="exp",
        name="top",
        description="Check the levelling leaderboard")
	async def top(self, ctx):
		users = db["guilds"][f"{ctx.guild.id}"]["users"]
		topusers = sorted(users.items(), key= lambda x: (x[1]['level'], x[1]['xp']), reverse=True)[:5]
		tosend = ""
		i = 0
		for user in topusers:
			try:
				name = ctx.guild.get_member(int(topusers[i][0]))
				level = topusers[i][1]['level']
				tosend += f"`{i+1}. {name} - Level {level}` \n"
			except:
				tosend += f"`{i+1}. No user found` \n"
			i += 1
		await prettysend(ctx, "Top level members", tosend)

def setup(bot):
    bot.add_cog(Levels(bot))