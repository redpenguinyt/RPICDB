import discord, json, traceback
from discord.ext.commands import AutoShardedBot

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not isinstance(msg.channel, discord.DMChannel) or getattr(msg.channel.permissions_for(msg.guild.me), "send_messages"):
            return
        await self.bot.process_commands(msg)

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