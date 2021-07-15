import discord, json
from discord.ext import commands
from utils import prettysend

class Config(commands.Cog):
	"""Configure the bot - Admin only"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="set a prefix")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def setprefix(self, ctx, prefix="$"):
		guilds = json.load(open('data/guilds.json', 'r'))
		if not guilds[f"{ctx.guild.id}"]:
			guilds[f"{ctx.guild.id}"] = {"prefix":prefix,"premium":False,"channelid":"","isLevels":True}
		else:
			guilds[f"{ctx.guild.id}"]["prefix"] = prefix
		json.dump(guilds, open('data/guilds.json', 'w'), indent=4)
		await prettysend(ctx, "Prefix set!")
	
	@commands.command(help="enable/disable the levelling system")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def togglelevels(self, ctx):
		guilds = json.load(open('data/guilds.json', 'r'))
		if not guilds[f"{ctx.guild.id}"]:
			guilds[f"{ctx.guild.id}"] = {"prefix":"$","premium":False,"channelid":"","isLevels":False}
		else:
			isEnabled = guilds[f"{ctx.guild.id}"]["isLevels"] == False

		guilds[f"{ctx.guild.id}"]["isLevels"] = isEnabled
		json.dump(guilds, open('data/guilds.json', 'w'), indent=4)

		newPreference = guilds[f"{ctx.guild.id}"]["isLevels"]
		await prettysend(ctx, f"Levelling preference changed to {newPreference}!")

def setup(bot):
	bot.add_cog(Config(bot))