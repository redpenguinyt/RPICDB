import discord, os
from discord.ext import commands
from discord_slash import cog_ext

class Logging(commands.Cog):
	""" Fun! FUn! FUN! """

	def __init__(self, bot):
		self.bot = bot

	@cog_ext.cog_subcommand(
		base="log",
        name="channel",
        description="Sends you a text file containing all messages in that channel")
	@commands.has_permissions(manage_messages=True)
	async def logchannel(self, ctx):
		if not ctx.author.guild_permissions.manage_messages:
			ctx.send("You don't have the right permissions ;-;", hidden=True)
			return
		messages = await ctx.channel.history().flatten()
		log = f"Messages in {ctx.channel.name}, starting with the latest message:\n\n"
		for item in messages:
			if item.clean_content == "":
				continue
			log += f"{item.author} > {item.clean_content}\n"

		file = open(f"{ctx.channel.id}.txt", "w+")
		file.write(str(log))
		file.close()
		with open(f"{ctx.guild.id}.txt", "r") as file:
			await ctx.author.send(file=discord.File(file, f"{ctx.guild.id}.txt"))
		await ctx.send("You recieved a DM with the log!", hidden=True)
		file.close()
		os.remove(f"{ctx.guild.id}.txt")

	
	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		print(f"{user} banned from {guild}")
	# Log ban and kick

def setup(bot):
	bot.add_cog(Logging(bot))