from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors
from utils import config, traceback_maker, getinfofromguild, prettysend
import discord

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config()
		bot.tree.on_error = self.on_app_command_error

	async def on_app_command_error(self, ctx, error):
		if isinstance(error, errors.MissingPermissions):
			await ctx.response.send_message("You don't have the right permissions!", ephemeral=True)
		else:
			await ctx.response.send_message(f"""
```An error occurred whilst processing your command. ;-;```
For help, and to report this as an issue, please join the testing server for this bot: <https://discord.gg/C9E5EqaHR8>
Also send the error message below:
{traceback_maker(error)}
			""", ephemeral=True)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		# Specifically to remove $help
		if isinstance(err, errors.CommandNotFound):
			return
		
		error = traceback_maker(err)
		await ctx.send(f"There was an error processing the command ;-; \n{error}")

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
		embed.set_thumbnail(url=member.avatar.url)
		embed.set_author(name=member.name,icon_url=member.avatar.url)
		embed.set_footer(text=member.guild, icon_url=member.guild.icon.url)
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
	async def on_ready(self):
		if not hasattr(self.bot, "uptime"):
			self.bot.uptime = datetime.utcnow()

		print(f"Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}")

async def setup(bot):
	await bot.add_cog(Events(bot))