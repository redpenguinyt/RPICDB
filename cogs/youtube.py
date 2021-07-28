import discord, os
from discord.ext import commands, tasks
from replit import db
from pyyoutube import Api
from utils import prettysend, config

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
	guilds = db["guilds"]
	with guilds[f"{guildid}"]["channelid"] as gcid:
		if f"{guildid}" in guilds:
			if gcid != "":
				return gcid
		else:
			return None

async def setchannelid(self, ctx, channelId=""):
	if channelId == "":
		await prettysend(ctx, "Disconnected YouTube Channel!")
	else:
		try:
			channel = getytchannel(channelId)["snippet"]["title"]
		except:
			await prettysend(ctx, "No channel found!")
		await prettysend(ctx, f"Connected to {channel}!")
	if not db["guilds"][f"{ctx.guild.id}"]:
		db["guilds"][f"{ctx.guild.id}"] = config["defaultguild"]
		db["guilds"]["{ctx.guild.id}"]["channelid"] = channelId
	else:
		db["guilds"][f"{ctx.guild.id}"]["channelid"] = channelId

class Youtube(commands.Cog):
	"""Youtube upload commands"""

	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		repeat.start(self)
	
@tasks.loop(minutes=10)
async def repeat(self):
	for guild in self.bot.guilds:
		if f"{guild.id}" in db["guilds"] and db["guilds"][f"{guild.id}"]["channelid"] != "":
			channelid = db["guilds"][f"{guild.id}"]["channelid"]
			channel = getytchannel(channelid)
			channelname = channel["snippet"]["title"]
			if isNewVideo(channelid):
				print(f"Task | A new video was uploaded by {channelname}!")
				result = api.get_activities_by_channel(channel_id=channelid, count=1).items[0]
				videoId = result.contentDetails.upload.videoId
				discordchannel = discord.utils.get(guild.text_channels, name="yt-uploads")
				if not channel:
					discordchannel = guild.system_channel
				sent = await discordchannel.send(f"**{channelname}** uploaded a new video! https://www.youtube.com/watch?v={videoId} @everyone")
				try: sent.publish()
				except: pass

def setup(bot):
    bot.add_cog(Youtube(bot))