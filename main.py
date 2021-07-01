import discord, os, app
from utils import Bot, config


config = config()
bot = Bot(
    command_prefix=config["prefix"], case_insensitive=True, prefix=config["prefix"],
    owner_ids=config["owners"], command_attrs=dict(hidden=True),
    allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),intents=discord.Intents(guilds=True, members=True, messages=True)
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

app.start()
try:
    bot.run(os.environ['token'])
except Exception as e:
    print(f"Error when logging in: {e}")