import discord
from discord.ext import commands
from utils import prettysend, load_json, write_json

class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	async def test(self,ctx):
		await prettysend(ctx, "I'm connected! :D")

	@commands.command(aliases=["load"], hidden=True)
	@commands.is_owner()
	async def load_cog(self, ctx, *, cog: str):
		try:
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=3.0)
		else:
			await ctx.send('**`SUCCESS`**', delete_after=3.0)

	@commands.command(aliases=["unload"], hidden=True)
	@commands.is_owner()
	async def unload_cog(self, ctx, *, cog: str):
		try:
			self.bot.unload_extension(cog)
		except Exception as e:
			await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=3.0)
		else:
			await ctx.send('**`SUCCESS`**', delete_after=3.0)
	
	@commands.command(aliases=["reload"], hidden=True)
	@commands.is_owner()
	async def reload_cog(self, ctx, *, cog: str):
		await self.unload_cog(self, ctx, cog)
		await self.load_cog(self, ctx, cog)
	
	@commands.command(hidden=True)
	@commands.guild_only()
	@commands.is_owner()
	async def renamechannel(self, ctx, *, new_name):
		await ctx.channel.edit(name=new_name)
		await ctx.message.delete()

	@commands.command(hidden=True, aliases=["role","giverole"])
	@commands.guild_only()
	@commands.is_owner()
	async def addrole(self, ctx, role, user: discord.Member):
		if not user:
			user = ctx.message.author
		try:
			await user.add_roles(discord.utils.get(user.guild.roles, name=role))
		except:
			await ctx.reply("Failed to execute",delete_after=1)
		await ctx.message.delete()
	
	@commands.command(hidden=True, aliases=["deleterole","delrole"])
	@commands.guild_only()
	@commands.is_owner()
	async def removerole(self, ctx, role, user: discord.Member):
		if not user:
			user = ctx.message.author
		await user.remove_roles(discord.utils.get(user.guild.roles, name=role))
		await ctx.message.delete()
	
	@commands.command(hidden=True)
	@commands.guild_only()
	@commands.is_owner()
	async def purge(self, ctx, limit: int = 5):
		await ctx.channel.purge(limit=limit + 1)

	@commands.command(hidden=True)
	@commands.guild_only()
	@commands.is_owner()
	async def getroles(self, ctx):
		roles = ctx.guild.roles
		tosend = f"Roles of {ctx.guild}: \n"
		for i in range(len(roles)):
			tosend += roles[i].name + "\n"
		try:
			await ctx.author.send(tosend)
		except:
			await ctx.send("Failed", delete_after=1)
		await ctx.message.delete()
    
	@commands.command(hidden=True, aliases=["debug"])
	@commands.is_owner()
	async def toggledebug(self, ctx):
		config = load_json("data/config.json")
		newsetting = config["debug"] == False
		
		config["debug"] = newsetting
		write_json("data/config.json", config)

		await ctx.reply(f"Debug set to {newsetting}!", delete_after=3)
		await ctx.message.delete()

def setup(bot):
	bot.add_cog(Owner(bot))