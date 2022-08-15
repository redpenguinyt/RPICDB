import discord
from discord.ext import commands
from utils import prettysend
from discord_slash import cog_ext

class Moderation(commands.Cog):
	"""Commands used to moderate your guild"""
	def __init__(self, bot):
		self.bot = bot

	async def __error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send(error)

	@cog_ext.cog_subcommand(
		base="mod",
		name="kick",
		description="Kick a user")
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member, reason="None specified"):
		if user.guild_permissions.manage_messages:
			return await ctx.send("That user has manage messages too!", hidden=True)
		try:
			await ctx.guild.kick(user,reason = f"By {ctx.author} for {reason}")
			await prettysend(ctx,
				"User kicked successfully",
				f"{user.mention} was kicked by {ctx.author} for {reason}"
			)
		except discord.Forbidden:
			return await ctx.send("Are you trying to kick someone higher than the bot?", hidden=True)

	@cog_ext.cog_subcommand(
		base="mod",
		name="ban",
		description="Ban a user")
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, reason="None specified"):
		if user.guild_permissions.manage_messages:
			return await ctx.send("That user has manage messages too!", hidden=True)
		try:
			await ctx.guild.ban(
				user, reason = f"By {ctx.author} for {reason}")
			await prettysend(ctx,
				"User banned successfully",
				f"{user.mention} was banned by {ctx.author} for {reason}"
			)
		except discord.Forbidden:
			return await ctx.send("Are you trying to ban someone higher than the bot", hidden=True)
	
	@cog_ext.cog_subcommand(
		base="mod",
		name="mute",
		description="Mutes the specified user")
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, user: discord.Member, reason="treason"):
		muted = discord.utils.get(ctx.guild.roles, name="Muted")
		if not muted:
			try:
				muted = await ctx.guild.create_role(name="Muted",reason="To use for muting")
				for channel in ctx.guild.channels:
					await channel.set_permissions(muted,send_messages=False,read_message_history=True,read_messages=True)
			except discord.Forbidden:
				return await ctx.send("I have no permissions to make a muted role")
			await user.add_roles(muted)
			await prettysend(ctx,
				"User muted successfully",
				f"{user.mention} was muted by {ctx.author} for {reason}"
			)
		else:
			try:
				await user.add_roles(muted)
				await prettysend(ctx,
					"User muted successfully",
					f"{user.mention} was muted by {ctx.author} for {reason}"
				)
			except discord.Forbidden:
				return await ctx.send("Are you trying to mute someone higher than the bot?", hidden=True)

	@cog_ext.cog_subcommand(
		base="mod",
		name="unmute",
		description="Unmute a user")
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, ctx, user: discord.Member):
		muted = discord.utils.get(ctx.guild.roles, name="Muted")
		if not muted in user.roles:
			await ctx.send("That user isn't muted!", hidden=True)
		else:
			try:
				await user.remove_roles(muted)
				await ctx.send(f"{user.mention} has been unmuted", hidden=True)
			except discord.Forbidden:
				return await ctx.send("Are you trying to unmute someone higher than the bot?", hidden=True)

	@cog_ext.cog_subcommand(
		base="mod",
		name="block",
		description="Block a user from the current channel")
	@commands.has_permissions(manage_channels=True)
	async def block(self, ctx, user: discord.Member):
		if user.guild_permissions.manage_messages:
			return await ctx.send("That user has manage messages too!", hidden=True)
		await ctx.channel.set_permissions(user, send_messages=False)
		await prettysend(ctx,
			"User blocked successfully",
			f"{user.mention} was muted by {ctx.author}"
		)

	@cog_ext.cog_subcommand(
		base="mod",
		name="unblock",
		description="Unblock a use from the current channel")
	@commands.has_permissions(manage_channels=True)
	async def unblock(self, ctx, user: discord.Member):
		await ctx.channel.set_permissions(user, send_messages=True)
		await ctx.send(f"{user.mention} has been unblocked", hidden=True)

	@cog_ext.cog_subcommand(
		base="mod",
		name="clear",
		description="Bulk remove messages from the current channel")
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, limit: int):
		await ctx.channel.purge(limit=limit)
		await ctx.send(f"Channel cleared of {limit} messages", hidden=True)

	@cog_ext.cog_subcommand(
		base="mod",
		name="nuke",
		description="nuke the channel and make a copy")
	@commands.has_permissions(manage_channels=True)
	async def nuke(self, ctx):
		await ctx.channel.clone()
		await ctx.channel.delete()

def setup(bot):
	bot.add_cog(Moderation(bot))
