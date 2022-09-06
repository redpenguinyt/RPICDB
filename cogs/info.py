import discord
from discord.ext import commands
from discord import app_commands
from utils import config, getinfofromguild

config = config()

def simpledate(target, clock=True):
    """ Clock format using datetime.strftime() """
    if not clock:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

class Info(commands.Cog):
	"""Simple commands"""

	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(description="Stop it. Get some help")
	async def help(self, ctx):
		description = """
Red Penguin Is Cool Discord Bot
RPICDB is the everything Discord bot for all your Discord needs!
Website: https://rpicdb.redpenguin.repl.co
Support: https://discord.gg/C9E5EqaHR8
		"""

		await ctx.response.send_message(
			embed=discord.Embed(
				color = 0xe74c3c,
				title = "RPICDB support!",
				description = description
			),
			ephemeral = True
		)

	info_group = app_commands.Group(name="info", description="Information commands")
	
	@info_group.command(description="Checks how many users are in the server")
	async def servercount(self, ctx):
		embed = discord.Embed(
			color=0xe74c3c,
			title = f"There are {ctx.guild.member_count} users in {ctx.guild.name}"
		)
		await ctx.response.send_message(embed=embed, ephemeral=True)

	
	@info_group.command(description="Get info about a user!")
	async def user(self, ctx, user: discord.Member):
		users = getinfofromguild(ctx.guild_id, "users")
		userinfo = {"level":1,"xp":0}
		if f"{user.id}" in users:
			userinfo = users[f"{user.id}"]
		lvl = userinfo['level']
		xp = userinfo["xp"]
		lvl_lmt = lvl * config["lvlmultiplier"]

		date_format = "%a, %d %b %Y %I:%M %p"
		members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
		role_string = ' '.join([r.mention for r in user.roles][1:])
		is_bot = "`No`"
		if user.bot: is_bot = "`Yes`"

		embed = discord.Embed(
			color = 0xe74c3c,
			title = "User Info"
		)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="User Name", value=f"`{user}`", inline=False)
		embed.add_field(name="Joined", value=f"`{user.joined_at.strftime(date_format)}`")
		embed.add_field(name="Join position", value=f"`{members.index(user)+1}`")
		embed.add_field(name="Registered", value=f"`{user.created_at.strftime(date_format)}`", inline=False)
		embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=f"{role_string}")
		embed.add_field(name="Bot", value=is_bot)
		embed.add_field(name="Mention", value=f"{user.mention}", inline=False)
		embed.add_field(name="Level", value=f"`{lvl}`")
		embed.add_field(name="XP",value=f"`{xp}/{lvl_lmt}`")
		embed.set_footer(text='ID: ' + f"{user.id}")

		await ctx.response.send_message(embed=embed, ephemeral=True)

	
	@info_group.command(description="Check info about current server")
	async def server(self, ctx):
		find_bots = sum(1 for member in ctx.guild.members if member.bot)

		embed = discord.Embed(
			color = 0xe74c3c,
			title = "Server Info"
		)

		if ctx.guild.icon:
			embed.set_thumbnail(url=ctx.guild.icon.url)
		if ctx.guild.banner:
			embed.set_image(url=ctx.guild.banner.url)
		embed.add_field(name="Server Name", value=f"`{ctx.guild.name}`", inline=False)
		embed.add_field(name="Members", value=f"`{ctx.guild.member_count}`")
		embed.add_field(name="Bots", value=f"`{find_bots}`")
		embed.add_field(name="Owner", value=f"`{ctx.guild.owner}`", inline=False)
		embed.add_field(name="Boost count", value=f"`{ctx.guild.premium_subscription_count}`")
		embed.add_field(name="Created", value=f"`{simpledate(ctx.guild.created_at)}`")
		embed.set_footer(text='ID: ' + f"{ctx.guild_id}")
		await ctx.response.send_message(embed=embed, ephemeral=True)

	
	@info_group.command(description="Check the bot's latency")
	async def ping(self, ctx):
		await ctx.response.send_message(
			embed=discord.Embed(
				title=f"Ping: {round(self.bot.latency * 1000)}ms"
			),
			ephemeral=True
		)


async def setup(bot):
	await bot.add_cog(Info(bot))