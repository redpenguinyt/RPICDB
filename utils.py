import discord, json, traceback
import pymongo
from secret_manager import MONGO_URL

client = pymongo.MongoClient(MONGO_URL)
channelsdb = client.RPICDB.yt_channels
afkdb = client.RPICDB.afk
guildsdb = client.RPICDB.guilds

def load_json(filename):
    with open(filename, encoding='utf-8') as infile:
        return json.load(infile)

def write_json(filename, contents):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)

def config():
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
		"test_guild_id": 858031893471559711,
	    "prefix": "$",
	    "lvlmultiplier": 50
	}

def update_channel(channelid, acts):
	if r := channelsdb.find_one_and_update({"_id": channelid}, {"$set": {"acts": acts}}):
		return r['acts']
	else:
		channelsdb.insert_one({
			'_id': channelid,
			'acts': acts
		})
		return None

def set_afk(userid, status):
	if status is None:
		afkdb.find_one_and_delete({'_id': userid})
	else:
		afkdb.find_one_and_update(
			{'_id': userid},
			{"$set":{'status': status}},
			upsert = True
		)

def get_afk(userid):
	return afkdb.find_one({'_id': userid})

def getinfofromguild(guildid, key):
	if guildsdb.find_one({"_id": guildid}):
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

async def prettysend(interaction, text, description=None):
	embed = discord.Embed(
		title = text,
		color=0xe74c3c
	)
	if description:
		embed.description = description
	await interaction.response.send_message(embed=embed)

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"