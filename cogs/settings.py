import discord
from discord.ext import commands
from utils import config, getinfofromguild
from cogs import youtube as yt
from discord_slash import cog_ext

class Settings(commands.Cog):
	"""Configure the bot - Administrator only"""

	def __init__(self, bot):
		self.bot = bot
	
	@cog_ext.cog_slash(description="Get a link to the dashboard")
	async def settings(self, ctx):
		await ctx.send("Go to https://rpicdb.redpenguin.repl.co/dashboard and log in with discord to make changes to settings in your bot!")
	
	@cog_ext.cog_subcommand(
		base="info",
        name="settings",
        description="Check your server's settings")
	async def settingsinfo(self, ctx):
		guild = getinfofromguild(ctx.guild.id, "all")

		# The user doesn't need to see these
		guild.pop("_id")
		guild.pop("users")
		guild.pop("premium")

		settings = "Edit your settings at https://rpicdb.redpenguin.repl.co/dashboard\n"
		for item in guild:
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