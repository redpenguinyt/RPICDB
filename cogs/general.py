import discord
from discord.ext import commands
from utils import prettysend

class General(commands.Cog):
	"""General commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Invite a user")
	async def invite(self, ctx, user: discord.User):
		await prettysend(ctx, "Invite sent!")
		invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
		await user.send("You have been invited to " + str(invitelink))

def setup(bot):
    bot.add_cog(General(bot))