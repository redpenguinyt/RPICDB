import discord
from discord.ext import commands
from utils import getinfofromguild
from discord import app_commands

class Settings(commands.Cog):
	"""Dashboard Portal"""

	def __init__(self, bot):
		self.bot = bot
	
	@app_commands.command(description="Check your server's settings")
	async def settings(self, ctx):
		guild = getinfofromguild(ctx.guild.id, "all")

		# The user doesn't need to see these
		guild.pop("_id")
		guild.pop("users")
		guild.pop("premium")

		settings = "Edit your settings at https://rpicdb.redpenguin.repl.co/dashboard\n"
		for item in guild:
			settings += f"**{item}**: {guild[item]}\n"
		await ctx.response.send_message(
			embed = discord.Embed(
				color=0xe74c3c,
				title="Settings",
				description=settings
			),
			ephemeral=True
		)

async def setup(bot):
	await bot.add_cog(Settings(bot))