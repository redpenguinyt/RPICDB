import discord
from discord.ext import commands
from utils import config
from cogs import youtube as yt
from replit import db
from discord_slash import cog_ext

async def toggleguildsetting(self, ctx, setting, userFriendlyName=""):
	if not db["guilds"][f"{ctx.guild.id}"]:
		db["guilds"][f"{ctx.guild.id}"] = config["defaultguild"]
	
	isEnabled = db["guilds"][f"{ctx.guild.id}"][setting] == False

	db["guilds"][f"{ctx.guild.id}"][setting] = isEnabled

	newPreference = db["guilds"][f"{ctx.guild.id}"][setting]
	await ctx.send(
		embed=discord.Embed(color=0xe74c3c,
			title=f"{userFriendlyName} setting changed to {newPreference}!"
		),
		hidden = True
	)

class Settings(commands.Cog):
	"""Configure the bot - Administrator only"""

	def __init__(self, bot):
		self.bot = bot
		self.config = config
	
	@cog_ext.cog_subcommand(
		base="settings",
        name="togglelevels",
        description="Toggle the levelling system in that server!")
	async def togglelevels(self, ctx):
		if not ctx.author.guild_permissions.administrator:
			ctx.send("You don't have the right permissions ;-;")
			return
		await toggleguildsetting(self, ctx, "isLevels", "Levelling")
	
	@cog_ext.cog_subcommand(
		base="settings",
        name="togglewelcome",
        description="Toggle the welcome message in that server!")
	async def togglewelcome(self, ctx):
		if not ctx.author.guild_permissions.administrator:
			ctx.send("You don't have the right permissions ;-;")
			return
		await toggleguildsetting(self, ctx, "isWelcome", "Welcome message")
	
	@cog_ext.cog_subcommand(
		base="settings",
        name="setchannelid",
        description="Set a YT channel id to get YouTube notifications!")
	async def setchannelid(self, ctx, channelid):
		if not ctx.author.guild_permissions.administrator:
			ctx.reply("You don't have the right permissions ;-;")
			return
		await yt.setchannelid(self, ctx, channelid)
	
	@cog_ext.cog_subcommand(
		base="info",
        name="settings",
        description="Check your server's settings")
	async def settings(self, ctx):
		guild = db["guilds"][f"{ctx.guild.id}"]
		settings = ""
		for item in guild:
			if item == "users":
				continue
			settings += f"**{item}**: {guild[item]}\n"
		await ctx.send(
			embed = discord.Embed(
				color=0xe74c3c,
				title="Settings",
				description=settings
			),
			hidden=True
		)

def setup(bot):
	bot.add_cog(Settings(bot))