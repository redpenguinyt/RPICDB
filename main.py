import discord, os
from discord.ext import commands
from keep_alive import keep_alive
import extra
bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():  # Console connect report
	print("Login as {0.user} in ".format(bot) + str(len(bot.guilds)) +
          " guilds")
	await bot.change_presence(activity=discord.Streaming(name="$help", url="http://www.twitch.tv/redpenguinyt"))

@bot.command()
async def test(ctx):
	await ctx.channel.send("I'm connected! :D")

@bot.command()
async def inspire(ctx):
	await ctx.channel.send(extra.get_quote())

@bot.command()
async def reverse(ctx, *args):
	response = ""
	for arg in args:
		response += " " + arg
	await ctx.channel.send(response[::-1])

keep_alive() # Keep bot alive
bot.run(os.getenv('TOKEN'))  # Send code to Discord