from discord.ext import commands

class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='load', hidden=True)
	@commands.is_owner()
	async def load_cog(self, ctx, *, cog: str):
		try:
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=3.0)
		else:
			await ctx.send('**`SUCCESS`**', delete_after=3.0)

	@commands.command(name='unload', hidden=True)
	@commands.is_owner()
	async def unload_load(self, ctx, *, cog: str):
		try:
			self.bot.unload_extension(cog)
		except Exception as e:
			await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=3.0)
		else:
			await ctx.send('**`SUCCESS`**', delete_after=3.0)
	
	@commands.command(name='reload', hidden=True)
	@commands.is_owner()
	async def reload_cog(self, ctx, *, cog: str):
		try:
			self.bot.unload_extension(cog)
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=3.0)
		else:
			await ctx.send('**`SUCCESS`**', delete_after=3.0)

def setup(bot):
	bot.add_cog(Owner(bot))