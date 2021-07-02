import discord, os, json
from utils import Bot, config

config = config()

async def determine_prefix(bot, message):
	prefixes = json.load(open('data/prefixes.json', 'r'))
	if f"{message.guild.id}" in prefixes:
		return prefixes[f"{message.guild.id}"]
	else:
		return config["prefix"]

bot = Bot(
    command_prefix=determine_prefix, case_insensitive=True, owner_ids=config["owners"], command_attrs=dict(hidden=True),
    allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),intents=discord.Intents(guilds=True, members=True, messages=True)
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


try:
    bot.run(os.environ['token'])
except Exception as e:
    print(f"Error when logging in: {e}")