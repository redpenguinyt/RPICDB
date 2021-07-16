import discord, os
from discord.ext import commands, tasks
from replit import db
from pyyoutube import Api
from utils import prettysend, config, load_json, write_json

config = config()
api = Api(api_key=os.environ['yt_api_key'])

def getytchannel(id):
	return api.get_channel_info(channel_id=id).items[0].to_dict()

def isNewVideo(channelid):
	acts = api.get_activities_by_channel(channel_id=channelid, count=1).items[0].contentDetails.upload.videoId
	if channelid in db["channels"]:
		prev_acts = db["channels"][channelid]
		db["channels"][channelid] = acts
	else:
		db["channels"][channelid] = acts
		return
	
	return acts != prev_acts

def guildChannelId(guildid):
	guilds = load_json("data/guilds.json")
	with guilds[f"{guildid}"]["channelid"] as gcid:
		if f"{guildid}" in guilds:
			if gcid != "":
				return gcid
		else:
			return None

async def setchannelid(self, ctx, channelId=""):
	guilds = load_json('data/guilds.json')
	if not guilds[f"{ctx.guild.id}"]:
		guilds[f"{ctx.guild.id}"] = config["defaultguild"]
		guilds["{ctx.guild.id}"]["channelid"] = "channelid"
	else:
		guilds[f"{ctx.guild.id}"]["channelid"] = channelId
	write_json('data/guilds.json', guilds)
	if channelId == "":
		await prettysend(ctx, "Disconnected YouTube Channel!")
	else:
		channel = getytchannel(channelId)["snippet"]["title"]
		await prettysend(ctx, f"Connected to {channel}!")

class Youtube(commands.Cog):
	"""Youtube upload commands"""

	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		repeat.start(self)
	
@tasks.loop(minutes=10)
async def repeat(self):
	guilds = load_json('data/guilds.json')
	for guild in self.bot.guilds:
		if f"{guild.id}" in guilds and guilds[f"{guild.id}"]["channelid"] != "":
			channelid = guilds[f"{guild.id}"]["channelid"]
			channel = getytchannel(channelid)
			channelname = channel["snippet"]["title"]
			if isNewVideo(channelid):
				print(f"Task | A new video was uploaded by {channelname}!")
				result = api.get_activities_by_channel(channel_id=channelid, count=1).items[0]
				videoId = result.contentDetails.upload.videoId
				discordchannel = discord.utils.get(guild.text_channels, name="yt-uploads")
				if not channel:
					discordchannel = guild.system_channel
				await discordchannel.send(f"**{channelname}** uploaded a new video! https://www.youtube.com/watch?v={videoId} @everyone")

def setup(bot):
    bot.add_cog(Youtube(bot))