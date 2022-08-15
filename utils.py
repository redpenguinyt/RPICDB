import discord, json, traceback, os
import pymongo

client = pymongo.MongoClient(os.environ['mongo_url'])
guildsdb = client.RPICDB.guilds

def load_json(filename):
    with open(filename, encoding='utf-8') as infile:
        return json.load(infile)

def write_json(filename, contents):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)

def config(filename: str = "config"):
    return {
	    "description": "Red Penguin Is Cool Discord Bot",
	    "owners": [
	        666323445453291561,
			714453553619664947
	    ],
	    "defaultguild": {
	        "premium": True,
	        "channelid": "",
	        "isLevels": True,
	        "isWelcome": True,
	        "users": {}
	    },
	    "prefix": "$",
	    "version": "0.9.5",
	    "lvlmultiplier": 50,
	    "debug": True
	}

def getinfofromguild(guildid, key):
	if guildsdb.find_one({"_id":guildid}):
		if key == "all":
			return guildsdb.find_one({"_id":guildid})
		return guildsdb.find_one({"_id":guildid})[key]
	else:
		addguildtocollection(guildid)
		return guildsdb.find_one({"_id":guildid})[key]

def addguildtocollection(guildid): # Don't use this in cogs
	newguild = config()["defaultguild"]
	newguild["_id"] = guildid
	guildsdb.insert_one(newguild)

def editguildinfo(guildid, key, newvalue):
	guildsdb.find_one_and_update(
		{"_id":guildid},
		{"$set":{key: newvalue}},
		upsert = True
	)

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