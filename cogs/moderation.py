import discord
from discord.ext import commands
from utils import prettysend
from discord import app_commands

class Moderation(commands.GroupCog, name="mod"):
	"""Commands used to moderate your guild"""
	def __init__(self, bot):
		self.bot = bot

	async def __error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.response.send_message(error)

	@app_commands.command(description="Kick a user")
	@app_commands.checks.has_permissions(kick_members=True)
	async def kick(self, ctx, user:discord.Member, reason:str="None specified"):
		if user.guild_permissions.manage_messages:
			return await ctx.response.send_message("That user has manage messages too!", ephemeral=True)
		try:
			await ctx.guild.kick(user,reason = f"By {ctx.user} for {reason}")
			await prettysend(ctx,
				"User kicked successfully",
				f"{user.mention} was kicked by {ctx.user} for {reason}"
			)
		except discord.Forbidden:
			return await ctx.response.send_message("Are you trying to kick someone higher than the bot?", ephemeral=True)

	@app_commands.command(description="Ban a user")
	@app_commands.checks.has_permissions(ban_members=True)
	async def ban(self, ctx, user:discord.Member, reason:str="None specified"):
		if user.guild_permissions.manage_messages:
			return await ctx.response.send_message("That user has manage messages too!", ephemeral=True)
		try:
			await ctx.guild.ban(
				user, reason = f"By {ctx.user} for {reason}")
			await prettysend(ctx,
				"User banned successfully",
				f"{user.mention} was banned by {ctx.user} for {reason}"
			)
		except discord.Forbidden:
			return await ctx.response.send_message("Are you trying to ban someone higher than the bot", ephemeral=True)
	
	@app_commands.command(description="Mutes the specified user")
	@app_commands.checks.has_permissions(manage_roles=True)
	async def mute(self, ctx, user:discord.Member, reason:str="treason"):
		muted = discord.utils.get(ctx.guild.roles, name="Muted")
		if not muted:
			try:
				muted = await ctx.guild.create_role(name="Muted",reason="To use for muting")
				for channel in ctx.guild.channels:
					await channel.set_permissions(muted,send_messages=False,read_message_history=True,read_messages=True)
			except discord.Forbidden:
				return await ctx.response.send_message("I have no permissions to make a muted role")
			await user.add_roles(muted)
			await prettysend(ctx,
				"User muted successfully",
				f"{user.mention} was muted by {ctx.user} for {reason}"
			)
		else:
			try:
				await user.add_roles(muted)
				await prettysend(ctx,
					"User muted successfully",
					f"{user.mention} was muted by {ctx.user} for {reason}"
				)
			except discord.Forbidden:
				return await ctx.response.send_message("Are you trying to mute someone higher than the bot?", ephemeral=True)

	@app_commands.command(
		description="Unmute a user")
	@app_commands.checks.has_permissions(manage_roles=True)
	async def unmute(self, ctx, user: discord.Member):
		muted = discord.utils.get(ctx.guild.roles, name="Muted")
		if not muted in user.roles:
			await ctx.response.send_message("That user isn't muted!", ephemeral=True)
		else:
			try:
				await user.remove_roles(muted)
				await ctx.response.send_message(f"{user.mention} has been unmuted", ephemeral=True)
			except discord.Forbidden:
				return await ctx.response.send_message("Are you trying to unmute someone higher than the bot?", ephemeral=True)

	@app_commands.command(
		description="Bulk remove messages from the current channel")
	@app_commands.checks.has_permissions(manage_messages=True)
	async def clear(self, ctx, limit: int):
		await ctx.channel.purge(limit=limit)
		await ctx.response.send_message(f"Channel cleared of {limit} messages", ephemeral=True)

	@app_commands.command(
		description="nuke the channel and make a copy")
	@app_commands.checks.has_permissions(manage_channels=True)
	async def nuke(self, ctx):
		await ctx.channel.clone()
		await ctx.channel.delete()

async def setup(bot):
	await bot.add_cog(Moderation(bot))