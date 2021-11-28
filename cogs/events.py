from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors
from utils import config, traceback_maker, getinfofromguild, prettysend
import discord

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config()

	@commands.Cog.listener()
	async def on_slash_command_error(self, ctx, error):
		if isinstance(error, errors.MissingPermissions):
			await ctx.send("You don't have the right permissions!", hidden=True)
		else:
			await ctx.send("""
```An error occurred whilst processing your command. ;-;```
For help, and to report this as an issue, please join the testing server for this bot: <https://discord.gg/C9E5EqaHR8>
Also send the error message below:
			""", hidden=True)
			if self.config["debug"]:
				await ctx.send(
					traceback_maker(error),
					hidden=True
				)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		# Specifically to remove $help
		if isinstance(err, errors.CommandNotFound):
			return
		
		error = traceback_maker(err)
		await ctx.send("There was an error processing the command ;-; ")
		if self.config["debug"]:
			await ctx.send(error)

	@commands.Cog.listener()
	async def on_message(self, msg):
		if f"<@!{self.bot.user.id}>" in msg.content:
			await msg.channel.send(f"Hi!")

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		if not getinfofromguild(member.guild.id, "isWelcome"):
			return

		channel = discord.utils.get(member.guild.text_channels, name="welcome")
		if not channel:
			channel = member.guild.system_channel
		embed = discord.Embed(
			title = "Welcome to our server!",
			description = f"{member.mention} has joined the server!",
			color=0xe74c3c
		)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_author(name=member.name,icon_url=member.avatar_url)
		embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
		embed.timestamp = datetime.utcnow()
		await channel.send(embed=embed)
		try:
			await member.send(f'Welcome to {member.guild.name}! We hope you enjoy the server')
		except:
			await prettysend(channel, f"{member} has DMs closed btw")

		role = discord.utils.get(member.guild.roles, name="Member")
		if role:
			await member.add_roles(role)

	@commands.Cog.listener()
	async def on_command(self, ctx):
		try:
			print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
		except AttributeError:
			print(f"Private message > {ctx.author} > {ctx.message.clean_content}")
	
	@commands.Cog.listener()
	async def on_slash_command(self, ctx):
		args = ""
		for i in ctx.args: args += f"{i}"

		command = f"/{ctx.name} {args}"
		if ctx.subcommand_name:
			command = f"{ctx.name} {ctx.subcommand_name} {args}"
		try:
			command = f"{ctx.guild.name} > {ctx.author} > {command}"
		except AttributeError:
			command = f"Private message > {ctx.author} > {command}"
		print(command)
		with open("commandlog.txt", "a") as myfile:
			myfile.write(f"\n{command}")

	@commands.Cog.listener()
	async def on_ready(self):
		if not hasattr(self.bot, "uptime"):
			self.bot.uptime = datetime.utcnow()

		print(f"Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}")

def setup(bot):
	bot.add_cog(Events(bot))