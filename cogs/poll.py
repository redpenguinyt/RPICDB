from discord.ext import commands
from discord_slash import cog_ext

def to_emoji(c):
	base = 0x1f1e6
	return chr(base + c)

class Polls(commands.Cog):
	"""Poll voting system."""

	def __init__(self, bot):
		self.bot = bot

	@cog_ext.cog_slash(description="Create a poll. To vote, use reactions!")
	async def poll(self, ctx, question, choice1, choice2, choice3="", choice4="", choice5=""):
		inputchoices = [choice1,choice2,choice3,choice4,choice5]
		for choice in inputchoices:
			if choice == "":
				inputchoices.pop(inputchoices.index(choice))

		perms = ctx.channel.permissions_for(ctx.me)
		if not (perms.read_message_history or perms.add_reactions):
			return await ctx.send('Need Read Message History and Add Reactions permissions.', hidden=True)

		choices = [(to_emoji(e), v) for e, v in enumerate(inputchoices)]
		choices.pop()

		body = "\n".join(f"{key}: {c}" for key, c in choices)
		poll = await ctx.send(f'{ctx.author.mention} asks: {question}\n\n{body}')
		for emoji, label in choices:
			await poll.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Polls(bot))