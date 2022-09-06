import discord, os
from discord import app_commands
from discord.ext import commands

class Logging(commands.GroupCog, name="log"):
	""" Fun! FUn! FUN! """

	def __init__(self, bot):
		self.bot = bot
		super().__init__()

	@app_commands.command(
        name="channel",
        description="Sends you a text file containing all messages in that channel")
	@app_commands.checks.has_permissions(manage_messages=True)
	async def logchannel(self, ctx, limit:int=None):
		log = f"Messages in {ctx.channel.name}, starting with the latest message:\n\n"
		async for msg in ctx.channel.history(limit=limit):
			if msg.clean_content == "":
				continue
			log += f"{msg.author} > {msg.clean_content}\n"

		file = open(f"{ctx.channel.id}.txt", "w+")
		file.write(str(log))
		file.close()
		with open(f"{ctx.channel.id}.txt", "r") as file:
			await ctx.user.send(file=discord.File(file, f"{ctx.channel.id}.txt"))
		await ctx.response.send_message("You recieved a DM with the log!", ephemeral=True)
		file.close()
		os.remove(f"{ctx.channel.id}.txt")

	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		await guild.owner.send(f"{user} banned from {guild}")
	# Log ban and kick

async def setup(bot):
	await bot.add_cog(Logging(bot))