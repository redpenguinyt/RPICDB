import discord
from discord.ext import commands


# This prevents staff members from being punished
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            raise commands.BadArgument("You cannot punish other staff members")


class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(
            ctx, argument)  # gets member object
        muted = discord.utils.get(ctx.guild.roles,
                                  name="Muted")  # gets role object
        if muted in argument.roles:  # checks if user has muted role
            return argument  # returns member object if there is muted role
        else:
            raise commands.BadArgument("The user was not muted.")


async def mute(ctx, user, reason):
    muted = discord.utils.get(ctx.guild.roles, name="Muted")
    hell = discord.utils.get(ctx.guild.text_channels, name="hell")
    if not muted:
        try:
            muted = await ctx.guild.create_role(name="Muted",
                                                reason="To use for muting")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted,
                                              send_messages=False,
                                              read_message_history=True,
                                              read_messages=True)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role")
        await user.add_roles(muted)
        await ctx.send(f"{user.mention} has been sent to hell for {reason}")
    else:
        await user.add_roles(muted)
        await ctx.send(f"{user.mention} has been sent to hell for {reason}")

    if not hell:
        overwrites = {
            ctx.guild.default_role:
            discord.PermissionOverwrite(read_message_history=False),
            ctx.guild.me:
            discord.PermissionOverwrite(send_messages=True),
            muted:
            discord.PermissionOverwrite(read_message_history=True)
        }
        try:
            channel = await ctx.guild.create_text_channel(
                'hell', overwrites=overwrites)
            await channel.send(
                "Welcome to hell.. You will spend your time here until you get unmuted. Enjoy the silence."
            )
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make #hell")


class Moderation(commands.Cog):
    """Commands used to moderate your guild"""
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    @commands.command(aliases=["banish"], help="ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Sinner = None, reason=None):

        if not user:
            return await ctx.send("You must specify a user")

        try:
            await ctx.guild.ban(
                user, f"By {ctx.author} for {reason}"
                or f"By {ctx.author} for None Specified")
            await ctx.channel.send(
                f"{user.mention} was banned by {ctx.message.author} for {reason}"
            )
        except discord.Forbidden:
            return await ctx.send(
                "Are you trying to ban someone higher than the bot")

    @commands.command(help="mute a user")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: Sinner, reason=None):
        await mute(ctx, user, reason or "treason")

    @commands.command(help="kick a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: Sinner = None, reason=None):
        if not user:
            return await ctx.send("You must specify a user")

        try:  # tries to kick user
            await ctx.guild.kick(user)
            await ctx.send(
                f"{ctx.author.mention} kicked {user.mention} for {reason}")
        except discord.Forbidden:
            return await ctx.send(
                "Are you trying to kick someone higher than the bot?")

    @commands.command(help="removes messages from channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, limit: int = 5):
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f"Bulk deleted `{limit}` messages", delete_after=3.0)

    @commands.command(help="unmute a user")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: Redeemed):
        await user.remove_roles(
            discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f"{user.mention} has been unmuted", delete_after=3.0)

    @commands.command(help="Warn a user for being bad")
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, *, reason="treason"):
        await ctx.channel.send(f"{member.mention} has been warned for {reason}"
                               )
        await member.send(f"You have been warned for {reason}")

    @commands.command(help="block a user from the current channel")
    @commands.has_permissions(manage_messages=True)
    async def block(self, ctx, user: Sinner = None):
        if not user:  # checks if there is user
            return await ctx.send("You must specify a user")

        await ctx.set_permissions(user, send_messages=False)

    @commands.command(help="unblock a use from the current channel")
    @commands.has_permissions(manage_messages=True)
    async def unblock(self, ctx, user: Sinner = None):
        if not user:  # checks if there is user
            return await ctx.send("You must specify a user")

        await ctx.set_permissions(user, send_messages=True)


def setup(bot):
    bot.add_cog(Moderation(bot))
