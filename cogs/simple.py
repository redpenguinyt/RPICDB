import discord
from discord.ext import commands

class General(commands.Cog):
	"""Simple commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Invite a user")
	async def invite(self, ctx, user: discord.User):
		await ctx.reply("Invite sent!")
		invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
		await user.send("You have been invited to " + str(invitelink))

def setup(bot):
    bot.add_cog(General(bot))