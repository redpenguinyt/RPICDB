import discord, json, traceback, os
from discord.ext.commands import AutoShardedBot
try:
	from pyyoutube import Api
except:
	os.system("pip install --upgrade python-youtube")
	from pyyoutube import Api

api = Api(api_key=os.environ['yt_api_key'])

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not isinstance(msg.channel, discord.DMChannel) or getattr(msg.channel.permissions_for(msg.guild.bot), "send_messages"):
            return
        await self.bot.process_commands(msg)

def isPremium(guildid):
	guilds = json.load(open('data/guilds.json', 'r'))
	if f"{guildid}" in guilds:
		return guilds[f"{guildid}"]["premium"] == True
	else:
		return False

def config(filename: str = "data/config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"