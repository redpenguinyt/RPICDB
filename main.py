import discord, time, os
from utils import config
from keep_alive import keep_alive
from discord.ext import commands
from discord import app_commands

config = config()
TEST_GUILD = discord.Object(id=config["test_guild_id"])

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class MyBot(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix = config["prefix"],
			owner_ids = config["owners"],
			help_command = None,
			intents = intents,
			activity = discord.Game(name="the saxaphone"), 
			application_id = 823590391302717510
		)

	async def setup_hook(self):
		# Load all cogs
		for file in os.listdir("cogs"):
			if file.endswith(".py"):
				await bot.load_extension(f"cogs.{file[:-3]}")

		await self.tree.sync()
		self.tree.copy_global_to(guild=TEST_GUILD)

bot = MyBot()

keep_alive()
while True:
	try:
		bot.run(os.environ['token'], reconnect=True)
	except Exception as e:
		print(f"Error when logging in: {str(e).split(': <!DOCT')[0]}")
	time.sleep(3)