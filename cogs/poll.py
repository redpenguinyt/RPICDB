from discord.ext import commands
from discord import app_commands

def to_emoji(c):
	base = 0x1f1e6
	return chr(base + c)

class Polls(commands.Cog):
	"""Poll voting system."""

	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(description="Create a poll. To vote, use reactions!")
	async def poll(self, ctx, question:str, choice1:str, choice2:str, choice3:str="", choice4:str="", choice5:str=""):
		inputchoices = [choice1,choice2,choice3,choice4,choice5]
		for choice in inputchoices:
			if choice == "":
				inputchoices.pop(inputchoices.index(choice))

		perms = ctx.channel.permissions_for(ctx.guild.me)
		if not (perms.read_message_history or perms.add_reactions):
			return await ctx.response.send_message('Need Read Message History and Add Reactions permissions.', ephemeral=True)

		choices = [(to_emoji(e), v) for e, v in enumerate(inputchoices)]
		choices.pop()

		body = "\n".join(f"{key}: {c}" for key, c in choices)
		await ctx.response.send_message(f'{ctx.user.mention} asks: {question}\n\n{body}')
		poll = await ctx.original_response()
		for emoji, label in choices:
			await poll.add_reaction(emoji)

async def setup(bot):
    await bot.add_cog(Polls(bot))