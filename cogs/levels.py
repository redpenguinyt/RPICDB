import discord, random
from discord.ext import commands
from utils import config, prettysend, getinfofromguild, guildsdb, addguildtocollection, editguildinfo
from discord import app_commands

config = config()

def edituserinfo(guildid, userid, content):
	guild = guildsdb.find_one(
		{"_id":guildid}
	)
	if not guild:
		guild = addguildtocollection(guildid)
	newusers = guild["users"][f"{userid}"] = content
	guildsdb.find_one_and_update(
		{"_id":guildid},
		{"$set":{"users": newusers}}
	)

def update_data(user: discord.Member):
	users = getinfofromguild(user.guild.id, "users")
	if not f"{user.id}" in users:
		users[f"{user.id}"] = {"xp":0,"level":1}
		editguildinfo(user.guild.id, "users", users)
	return users

def add_xp(user: discord.Member, exp):
	users = update_data(user)
	users[f"{user.id}"]['xp'] += exp
	editguildinfo(user.guild.id, "users", users)

def remove_xp(user: discord.Member, exp):
	users = update_data(user)
	users[f"{user.id}"]['xp'] -= exp
	editguildinfo(user.guild.id, "users", users)

async def level_up(user: discord.Member, ctx):
	users = getinfofromguild(user.guild.id, "users")
	old_lvl = users[f"{user.id}"]['level']
	lvl_lmt = old_lvl * config["lvlmultiplier"]
	
	while users[f"{user.id}"]['xp'] >= lvl_lmt:
		users[f"{user.id}"]['xp'] = users[f"{user.id}"]['xp'] - lvl_lmt
		users[f"{user.id}"]['level'] += 1
		old_lvl += 1
		
	if users[f"{user.id}"]['level'] != old_lvl:
		embed = discord.Embed(
			title = "Level Up!",
			description = f"GG, {user.mention}! You\'ve leveled up to level {users[f'{user.id}']['level']}",
			color=0xe74c3c
		)
		embed.set_thumbnail(url=user.avatar.url)
		await ctx.channel.send(embed=embed)
	
	editguildinfo(ctx.guild.id, "users", users)

		
	
class Levels(commands.GroupCog, name="exp"):
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
			add_xp(msg.author, random.randint(3,8))
			await level_up(msg.author, msg)
	
	@app_commands.command(
        name="give",
        description="Give XP to a user")
	@app_commands.checks.has_permissions(manage_messages=True)
	async def givexp(self, ctx, amount: int, user: discord.Member=None):
		user = user or ctx.user

		add_xp(user, amount)
		await level_up(user, ctx)

		await ctx.response.send_message(f"Gave {amount} XP to {user.mention}",ephemeral=True)
	
	@app_commands.command(
        name="remove",
        description="Take XP from a user")
	@app_commands.checks.has_permissions(manage_messages=True)
	async def removexp(self, ctx, amount: int, user: discord.Member=None):
		user = user or ctx.user

		remove_xp(user, amount)
		await level_up(user, ctx)

		await ctx.response.send_message(f"Took {amount} XP from {user.mention}",ephemeral=True)

	@app_commands.command(
        name="top",
        description="Check the levelling leaderboard")
	async def topxp(self, ctx):
		users = getinfofromguild(ctx.guild.id, "users")
		topusers = sorted(users.items(), key= lambda x: (x[1]['level']), reverse=True)[:5]
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

async def setup(bot):
    await bot.add_cog(Levels(bot))