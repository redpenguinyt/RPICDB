from discord.ext import commands
from discord_slash import cog_ext
from replit import db as replitdb
import discord

def setAFK(userid, status):
	if status == None:
		replitdb["afk"].pop(f"{userid}")
		return
	replitdb["afk"][f"{userid}"] = status

def getAFK(userid):
	if f"{userid}" in replitdb["afk"]:
		return replitdb["afk"][f"{userid}"]
	else:
		return None

class Drion(commands.Cog):
	""" A cog dedicated to Kingdrom of Drion """

	def __init__(self, bot):
		self.bot = bot
	
	@cog_ext.cog_slash(description="Set yourself as afk")
	async def afk(self, ctx, status=""):
		if getAFK(ctx.author.id) is not None:
			setAFK(ctx.author.id, None)
			await ctx.send("You are no longer afk", hidden=True)
		else:
			setAFK(ctx.author.id, status)
			await ctx.send(f'You are now [afk]. Send a message again in chat to remove afk status', hidden=True)
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if getAFK(msg.author.id) is not None:
			setAFK(msg.author.id, None)
			await msg.channel.send(f"Welcome back {msg.author.mention}! You are no longer AFK")
		for member in msg.mentions:
			status = getAFK(member.id)
			if status is not None:
				tosend = f"{member.display_name} is AFK"
				if status != "":
					tosend += f": {status}"
				await msg.reply(tosend)

def setup(bot):
	bot.add_cog(Drion(bot))