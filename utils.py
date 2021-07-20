import discord, json, traceback

def load_json(filename):
    with open(filename, encoding='utf-8') as infile:
        return json.load(infile)

def write_json(filename, contents):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)

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

async def prettysend(ctx, text, description=None):
	embed = discord.Embed(
		title = text,
		color=0xe74c3c
	)
	if description:
		embed.description = description
	await ctx.send(embed=embed)

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"