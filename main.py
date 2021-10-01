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

@bot.command()
@commands.is_owner()
async def updatereadme(ctx):
	maintxt = """
# RPICDB
RPICDB is the everything discord bot for you your everything discord needs! It also supports slash commands! Neato!

Check out what I'm working on now on the [github project](https://github.com/redpenguinyt/Discord-bot/projects/1)

### Features:

* Mod commands - mute, clear, block, nuke, kick and ban
* Toggleable levelling system with leaderboard
* Fun commands! Memes, poop, rickrolls!
* Utility commands! Get information about users and your server, and more!
* Youtube notifications! Set a yt channel id and get notified of your favourite youtuber's uploads!
* Polls! Create reaction polls
* A welcome message!

### Commands:
	"""
	allcommands = await slash.to_dict()
	for cmd in allcommands["global"]:
		cmd_to_txt = "* `"
		if cmd["options"] == []:
			cmd_to_txt += f"/{cmd['name']}` - {cmd['description']}"
			maintxt += f"\n{cmd_to_txt}"
		elif cmd["description"] == 'No Description.':
			for subcmd in cmd["options"]:
				cmd_to_txt = "* `"
				if subcmd["options"] == []:
					cmd_to_txt += f"/{cmd['name']} {subcmd['name']}` - {subcmd['description']}"
				else:
					cmd_to_txt += f"/{cmd['name']} {subcmd['name']}"
					for option in subcmd["options"]:
						if option["required"]:
						 	cmd_to_txt += f" <{option['name']}>"
						else:
						 	cmd_to_txt += f" [{option['name']}]"
					cmd_to_txt += f"` - {subcmd['description']}"
				maintxt += f"\n{cmd_to_txt}"
		else:
			cmd_to_txt += f"/{cmd['name']}"
			for option in cmd["options"]:
				if option["required"]:
					cmd_to_txt += f" <{option['name']}>"
				else:
					cmd_to_txt += f" [{option['name']}]"
			cmd_to_txt += f"` - {cmd['description']}"
			maintxt += f"\n{cmd_to_txt}"
	maintxt += "\n\nBy the way RPICDB stands for Red Penguin Is Cool Discord Bot"
	with open("README.md", 'w') as file:
		file.write(maintxt)
	await ctx.send("Done!")


keep_alive()
try:
	bot.run(os.environ['token'], reconnect=True)
except Exception as e:
	print(f"Error when logging in: {e}")