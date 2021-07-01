import discord
from discord.ext import commands

def simpledate(target, clock=True):
    """ Clock format using datetime.strftime() """
    if not clock:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

class Info(commands.Cog):
    """Simple commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def server(self, ctx):
        """ Check info about current server """
        if ctx.invoked_subcommand is None:
            find_bots = sum(1 for member in ctx.guild.members if member.bot)

            embed = discord.Embed()

            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon_url)
            if ctx.guild.banner:
                embed.set_image(url=ctx.guild.banner_url_as(format="png"))

            embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=find_bots, inline=True)
            embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            embed.add_field(name="Created", value=simpledate(ctx.guild.created_at), inline=True)
            await ctx.reply(content=f"ℹ information about **{ctx.guild.name}**", embed=embed)

    @commands.command(name='rickroll')
    async def example_embed(self, ctx):
        embed = discord.Embed(title='Rickroll',description='Never gonna give you up',colour=0x98FB98)
        embed.set_author(name=ctx.author.name,url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',icon_url=ctx.author.avatar_url)
        embed.set_image(url='https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif')

        embed.add_field(name='Subscribe', value='[Click Here!](https://youtube.com/watch?v=dQw4w9WgXcQ/)')
        embed.set_footer(text='Made in Python', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**Rickroll**', embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))