import discord
from discord.ext import commands
from utils import config, prettysend
from replit import db

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

	@commands.command(aliases=["level","user"],help="get info about a user or yourself!")
	@commands.guild_only()
	async def userinfo(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.message.author
		userinfo = {"level":1,"xp":0}
		if f"{user.id}" in db["users"]:
			userinfo = db["users"][f"{user.id}"]
		lvl = userinfo['level']
		xp = userinfo["xp"]
		lvl_lmt = lvl * config["lvlmultiplier"]

		date_format = "%a, %d %b %Y %I:%M %p"
		members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
		role_string = ' '.join([r.mention for r in user.roles][1:])

		embed = discord.Embed(color=0xe74c3c)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_author(name=f"{user}",icon_url=user.avatar_url)
		embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
		embed.add_field(name="Join position", value=f"{members.index(user)+1}")
		embed.add_field(name="Registered", value=f"{user.created_at.strftime(date_format)}")
		embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
		embed.add_field(name="Level", value=lvl)
		embed.add_field(name="XP",value=f"{xp}/{lvl_lmt}")
		embed.set_footer(text='ID: ' + f"{user.id}")

		await ctx.reply(embed=embed)

	@commands.command(help="get info about a server",aliases=["server"])
	@commands.guild_only()
	async def serverinfo(self, ctx):
		""" Check info about current server """
		if ctx.invoked_subcommand is None:
			find_bots = sum(1 for member in ctx.guild.members if member.bot)

			embed = discord.Embed(color=0xe74c3c)

			if ctx.guild.icon:
				embed.set_thumbnail(url=ctx.guild.icon_url)
			if ctx.guild.banner:
				embed.set_image(url=ctx.guild.banner_url_as(format="png"))

			embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
			embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
			embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
			embed.add_field(name="Bots", value=find_bots, inline=True)
			embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
			embed.add_field(name="Region", value=ctx.guild.region, inline=True)
			embed.add_field(name="Created", value=simpledate(ctx.guild.created_at), inline=True)
			await ctx.reply(embed=embed)

	@commands.command(help="check your ping")
	async def ping(self, ctx):
		await prettysend(ctx, f"{ctx.author.mention}\'s: {round(self.bot.latency * 1000)}",delete_after=3.0)
		await ctx.message.delete()

def setup(bot):
	bot.add_cog(Info(bot))