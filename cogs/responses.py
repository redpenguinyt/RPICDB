import discord
from discord.ext import commands
from discord import app_commands
from utils import config

config = config()

class Responses(commands.Cog):
	"""Responding to various messages"""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, msg: discord.Message):
		content = msg.content.lower().strip()

		if self.bot.user in msg.mentions:
			if msg.author.bot:
				await msg.reply("Silence, bot")
			else:
				await msg.reply("Hi! Please use the RPICDB /help command")

		await self.bot.process_commands(msg)

async def setup(bot):
	await bot.add_cog(Responses(bot))