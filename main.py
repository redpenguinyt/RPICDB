import discord, os
from utils import config, determine_prefix
from keep_alive import keep_alive
from discord.ext import commands

config = config()

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

bot = commands.Bot(
    command_prefix=determine_prefix,
	help_command = MyHelpCommand(),
	description="",
	case_insensitive=True,
	owner_ids=config["owners"],
	command_attrs=dict(hidden=True),
    allowed_mentions=discord.AllowedMentions(
		roles=True, users=True, everyone=False),
	intents=discord.Intents(guilds=True, members=True, messages=True)
)

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