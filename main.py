import discord, os
from utils import config
from keep_alive import keep_alive
from discord.ext import commands
from discord_slash import SlashCommand

config = config()

bot = commands.Bot(
    command_prefix = config["prefix"],
	owner_ids = config["owners"],
	help_command = None,
	intents = discord.Intents().all(),
	activity=discord.Game(name="the saxaphone")
)

slash = SlashCommand(bot, sync_commands=True)

# Load all cogs
for file in os.listdir("cogs"):
	if file.endswith(".py"):
		name = file[:-3]
		bot.load_extension(f"cogs.{name}")

keep_alive()
try:
	bot.run(os.environ['token'], reconnect=True)
except Exception as e:
	print(f"Error when logging in: {e}")