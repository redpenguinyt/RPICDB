import discord, pyyoutube
from discord.ext import commands, tasks
from utils import config, getinfofromguild, update_channel
from secret_manager import YT_API_KEY

config = config()
api = pyyoutube.Api(
	api_key=YT_API_KEY
)

def getytchannel(id):
	return api.get_channel_info(channel_id=id).items[0].to_dict()

def isNewVideo(channelid):
	acts = api.get_activities_by_channel(channel_id=channelid, count=1).items[0].contentDetails.upload.videoId
	acts = update_channel(channelid, prev_acts := acts)
	if acts == None:
		return False

	return acts != prev_acts

class Youtube(commands.Cog):
	"""Youtube upload commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		checkforupload.start(self)

@tasks.loop(minutes=10)
async def checkforupload(self):
	for guild in self.bot.guilds:
		guildchannelid = getinfofromguild(guild.id, "channelid")
		if guildchannelid != "":
			channel = getytchannel(guildchannelid)
			channelname = channel
			if isNewVideo(guildchannelid):
				print(f"Task | A new video was uploaded by {channelname}!")
				result = api.get_activities_by_channel(channel_id=guildchannelid, count=1).items[0]
				videoId = result.contentDetails.upload.videoId
				discordchannel = discord.utils.get(guild.text_channels, name="yt-uploads")
				if not discordchannel:
					discordchannel = guild.system_channel
				if not discordchannel:
					discordchannel = guild.text_channels[0]
				sent = await discordchannel.send(f"**{channelname}** uploaded a new video! https://www.youtube.com/watch?v={videoId} @everyone")
				try: await sent.publish()
				except: pass

async def setup(bot):
    await bot.add_cog(Youtube(bot))