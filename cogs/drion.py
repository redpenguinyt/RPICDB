from discord.ext import commands
from discord import app_commands
from replit import db

def setAFK(userid, status):
	if status == None:
		db["afk"].pop(f"{userid}")
		return
	db["afk"][f"{userid}"] = status

def getAFK(userid):
	if f"{userid}" in db["afk"]:
		return db["afk"][f"{userid}"]
	else:
		return None

class Drion(commands.Cog):
	""" A cog dedicated to Kingdrom of Drion """

	def __init__(self, bot):
		self.bot = bot
	
	@app_commands.command(description="Set yourself as afk")
	async def afk(self, ctx, status: str=""):
		if getAFK(ctx.user.id) is not None:
			setAFK(ctx.user.id, None)
			await ctx.response.send_message("You are no longer afk", ephemeral=True)
		else:
			setAFK(ctx.user.id, status)
			await ctx.response.send_message(f'You are now [afk]. Send a message again in chat to remove afk status', ephemeral=True)
	
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

async def setup(bot):
	await bot.add_cog(Drion(bot))