import discord, json, random
from discord.ext import commands

def update_data(users, user: discord.User):
	if not f'{user.id}' in users:
		users[f'{user.id}'] = {}
		users[f'{user.id}']['experience'] = 0
		users[f'{user.id}']['level'] = 1
	return users


def add_experience(users, user: discord.User, exp):
	users[f'{user.id}']['experience'] += exp
	return users


async def level_up(users, user: discord.User, msg):
	experience = users[f'{user.id}']['experience']
	lvl = users[f'{user.id}']['level']
	lvl_lmt = lvl * 12
	if experience >= lvl_lmt:
		await msg.channel.send(f'{user.mention} has leveled up to level {lvl + 1}')
		users[f'{user.id}']['level'] = lvl + 1
		users[f'{user.id}']['experience'] = experience - lvl_lmt
	return users

class Levels(commands.Cog):
	"""Levels"""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		users = json.load(open('data/users.json', 'r'))

		update_data(users, member)

		json.dump(users, open('data/users.json', 'w'))


	@commands.Cog.listener()
	async def on_message(self, msg):
		if not msg.author.bot:
			users = json.load(open('data/users.json', 'r'))

			update_data(users, msg.author)
			add_experience(users, msg.author, random.randint(3,8))
			await level_up(users, msg.author, msg)

			json.dump(users, open('data/users.json', 'w'))

		await self.bot.process_commands(msg)

	@commands.command(help="check your level!")
	async def level(self, ctx, member: discord.Member = None):
		if not member:
			id = ctx.message.author.id
			with open('data/users.json', 'r') as f:
				users = json.load(f)
			lvl = users[str(id)]['level']
			await ctx.reply(f'You are at level {lvl}!')
		else:
			id = member.id
			with open('data/users.json', 'r') as f:
				users = json.load(f)
			lvl = users[str(id)]['level']
			await ctx.reply(f'{member} is at level {lvl}!')

def setup(bot):
    bot.add_cog(Levels(bot))