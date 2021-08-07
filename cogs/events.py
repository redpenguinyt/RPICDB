import discord, os, psutil
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors
from utils import config, traceback_maker, getinfofromguild, prettysend

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config()
		self.process = psutil.Process(os.getpid())

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
			helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
			await ctx.send(helper)

		elif isinstance(err, errors.CommandInvokeError):
			error = traceback_maker(err.original)
			if "Missing Permissions" in str(err).lower():
				return await ctx.send("Command error! Missing permissions!")

			if "2000 or fewer" in str(err) and len(ctx.message.clean_content) > 1900:
				return await ctx.send(
					"You attempted to make the command display more than 2,000 characters...\n"
					"Both error and command will be ignored."
				)

			await ctx.send("There was an error processing the command ;-; ")
			if self.config["debug"]:
				await ctx.send(error)

		elif isinstance(err, errors.CheckFailure):
			pass

		elif isinstance(err, errors.MaxConcurrencyReached):
			await ctx.send("You've reached max capacity of command usage at once, please finish the previous one...")

		elif isinstance(err, errors.CommandOnCooldown):
			await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.2f} seconds.")
		elif isinstance(err, errors.CommandNotFound):
			pass

	@commands.Cog.listener()
	async def on_message(self, msg):
		if f"<@!{self.bot.user.id}>" in msg.content and "prefix" in msg.content.lower():
			try:
				prefix = getinfofromguild(msg.guild.id, "prefix")
			except:
				prefix = config["prefix"]
			await msg.channel.send(f"My prefix is {prefix}")

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		print(f"{member.guild.name} > {member} > Joined the guild")
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
			prettysend(channel, f"{member} has DMs closed btw")

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
	async def on_ready(self):
		if not hasattr(self.bot, "uptime"):
			self.bot.uptime = datetime.utcnow()

		# Check if user desires to have something other than online
		status = self.config["status_type"].lower()
		status_type = {"idle": discord.Status.idle, "dnd": discord.Status.dnd}

		# Check if user desires to have a different type of activity
		activity = self.config["activity_type"].lower()
		activity_type = {"listening": 2, "watching": 3, "competing": 5}

		await self.bot.change_presence(
			activity=discord.Game(
				type=activity_type.get(activity, 0), name=self.config["activity"]
			),
			status=status_type.get(status, discord.Status.online)
		)

		print(f"Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}")
#		print(self.bot.guilds)

def setup(bot):
	bot.add_cog(Events(bot))