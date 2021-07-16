import discord, json, traceback, os
from pyyoutube import Api

api = Api(api_key=os.environ['yt_api_key'])

def getinfofromguild(guildid, key):
	guilds = json.load(open('data/guilds.json', 'r'))
	if f"{guildid}" in guilds:
		return guilds[f"{guildid}"][key]
	else:
		return

def config(filename: str = "data/config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

async def determine_prefix(bot, message):
	try:
		prefixes = json.load(open('data/guilds.json', 'r'))
		return [prefixes[f"{message.guild.id}"]["prefix"],"$"]
	except:
		return config["prefix"]

async def prettysend(ctx, text):
	embed = discord.Embed(
		title = text,
		color=0xe74c3c
	)
	await ctx.reply(embed=embed)

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"