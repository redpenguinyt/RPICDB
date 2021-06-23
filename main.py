import discord, os, random
from discord.ext import commands
from keep_alive import keep_alive
import extra

client = discord.Client()
bot = commands.Bot(command_prefix="$",case_insensitive=True)

@bot.event
async def on_ready():  # Console connect report
	print("Login as {0.user} in ".format(bot) + str(len(bot.guilds)) + " guilds")
	await bot.change_presence(activity=discord.Streaming(name="$help", url="http://www.twitch.tv/redpenguinyt"))

@bot.command(help="test the bot's connection")
async def test(ctx):
	await ctx.reply("I'm connected! :D", delete_after=3.0)

@bot.command(help="recieve an inspirational quote!")
async def inspire(ctx):
	await ctx.reply(extra.get_quote(), delete_after=3.0)

@bot.command(help="reverse whatever you say!")
async def reverse(ctx, *, message):
	await ctx.reply(message[::-1], delete_after=3.0)

@bot.command(help="compliment someone!")
async def compliment(ctx, target):
	await ctx.channel.send(random.choice(extra.hapwrds) % target)

@bot.command(help="Warn a user for being bad - Coolbois and Admins only", brief="Warn a user for being bad")
async def warn(ctx, member: discord.User, *, content):
	await ctx.channel.send(extra.mentionusr(member) + " has been warned for " + content)
	await member.send("You have been warned for " + content)

@bot.command(help="get info about a user")
async def userinfo(ctx: commands.Context, user: discord.User):
	user_id = user.id
	username = user.name
	avatar = user.avatar.url
	await ctx.send(f'User found: {user_id} -- {username}\n{avatar}')
@userinfo.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.BadArgument):
        return await ctx.send('Couldn\'t find that user.')

#keep_alive() # Keep bot alive [disabled for now]
bot.run(os.getenv('TOKEN'))  # Send code to Discord