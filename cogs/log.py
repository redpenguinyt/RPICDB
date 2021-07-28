import discord
from discord.ext import commands

class Fun(commands.Cog):
	""" Fun! FUn! FUN! """

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="logs the current channel")
	@commands.has_permissions(manage_messages=True)
	async def logchannel(self, ctx):
		messages = await ctx.channel.history().flatten()
		log = f"Messages in {ctx.channel.name}, starting with the latest message:\n"
		for item in messages:
			log += f"{item.clean_content}\n"
		await ctx.author.send(str(log))
		await ctx.reply("You recieved a DM with the log!")

def setup(bot):
	bot.add_cog(Fun(bot))