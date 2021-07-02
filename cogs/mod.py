import discord, json
from discord.ext import commands
from utils import config

config = config()

class Moderator(commands.Cog):
	"""Example commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Warn a user for being bad",)
	@commands.guild_only()

	async def warn(self, ctx, member: discord.User, *, reason="[no reason specified]"):
		await ctx.channel.send(
			f"{member.mention} has been warned for {reason}")
		await member.send(f"You have been warned for {reason}")
	
	@commands.command(help="set a prefix")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def setprefix(self, ctx, prefix=None):
		prefixes = json.load(open('data/prefixes.json', 'r'))
		prefixes[ctx.guild.id] = prefix or config["prefix"]
		json.dump(prefixes, open('data/prefixes.json', 'w'))
		await ctx.reply("Prefix set!", delete_after=3.0)

	@commands.command(help="mute a user")
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, user: discord.User, *, reason="[no reason specified]"):
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		await commands.add_roles(user, role)
		ctx.channel.send(
		    f"{user.mention} has been muted by {ctx.message.author} for {reason}")
	
	@commands.command(help="remove the last few messages in this channel")
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount=5):
		await ctx.channel.purge(limit=amount + 1)

def setup(bot):
    bot.add_cog(Moderator(bot))