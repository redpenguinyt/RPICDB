import discord, random
from discord.ext import commands
from utils import prettysend

class General(commands.Cog):
	"""General commands"""

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(help="Check where to hide toxic waste")
	async def wheretohidetoxicwaste(self, ctx):
		randomx = random.randint(-160,160)
		randomy = random.randint(-160,160)
		where = f"https://www.google.com/maps/@{randomx},{randomy},10z"
		await prettysend(ctx, f"Here: {where}")

def setup(bot):
    bot.add_cog(General(bot))