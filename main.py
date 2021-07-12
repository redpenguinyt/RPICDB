import discord, os, json
from utils import Bot, config
from keep_alive import keep_alive

config = config()

async def determine_prefix(bot, message):
	try:
		prefixes = json.load(open('data/guilds.json', 'r'))
		return prefixes[f"{message.guild.id}"]["prefix"]
	except:
		return config["prefix"]

bot = Bot(
    command_prefix=determine_prefix, case_insensitive=True, owner_ids=config["owners"], command_attrs=dict(hidden=True),
    allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),intents=discord.Intents(guilds=True, members=True, messages=True)
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

keep_alive()
try:
    bot.run(os.environ['token'])
except Exception as e:
    print(f"Error when logging in: {e}")