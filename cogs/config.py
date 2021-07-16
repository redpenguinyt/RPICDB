import discord
from discord.ext import commands
from utils import prettysend, config, load_json, write_json
from cogs import youtube as yt

async def toggleguildsetting(self, ctx, setting, userFriendlyName=""):
	guilds = load_json('data/guilds.json')
	if not guilds[f"{ctx.guild.id}"]:
		guilds[f"{ctx.guild.id}"] = config["defaultguild"]
		guilds[f"{ctx.guild.id}"] = config["defaultguild"]
	else:
		isEnabled = guilds[f"{ctx.guild.id}"][setting] == False

	guilds[f"{ctx.guild.id}"][setting] = isEnabled
	write_json('data/guilds.json',guilds)

	newPreference = guilds[f"{ctx.guild.id}"][setting]
	await prettysend(ctx, f"{userFriendlyName} Setting changed to {newPreference}!")

class Settings(commands.Cog):
	"""Configure the bot - Admin only"""

	def __init__(self, bot):
		self.bot = bot
		self.config = config

	@commands.command(help="set a prefix")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def setprefix(self, ctx, prefix="$"):
		guilds = load_json("data/guilds.json")
		if not guilds[f"{ctx.guild.id}"]:
			guilds[f"{ctx.guild.id}"] = config["defaultguild"]
			guilds[f"{ctx.guild.id}"]["prefix"] = prefix
		else:
			guilds[f"{ctx.guild.id}"]["prefix"] = prefix
		write_json('data/guilds.json',guilds)
		await prettysend(ctx, "Prefix set!")
	
	@commands.command(help="enable/disable the levelling system")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def togglelevels(self, ctx):
		await toggleguildsetting(self, ctx, "isLevels", "Levelling")
	
	@commands.command(help="enable/disable the default welcome message")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def togglewelcome(self, ctx):
		await toggleguildsetting(self, ctx, "isWelcome", "Welcome message")
	
	@commands.command(help="set a yt channel id to be notified of uploads")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def setchannelid(self, ctx, channelid=""):
		yt.setchannelid(self, ctx, channelid="")

def setup(bot):
	bot.add_cog(Settings(bot))