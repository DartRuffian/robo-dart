# Discord Imports
import discord
from discord.ext import commands
from discord.utils import get


class Auto_Welcomer(commands.Cog):
    """ Auto Welcomer """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_embed = discord.Embed (
            description=f"Everyone please welcome {member.mention} to {member.guild.name}!",
            color=0x1dfd00
        )
        welcome_embed.set_thumbnail(url=member.avatar_url)
        welcome_channel = get(member.guild.channels, name="welcome")
        if welcome_channel is not None:
            await welcome_channel.send(embed=welcome_embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome_embed = discord.Embed (
            description=f"Sorry to see you go {member.mention}, hope to see you again!",
            color=0xFF0000
        )
        welcome_embed.set_thumbnail(url=member.avatar_url)
        welcome_channel = get(member.guild.channels, name="welcome")
        if welcome_channel is not None:
            await welcome_channel.send(embed=welcome_embed)


def setup(bot):
    bot.add_cog(Auto_Welcomer(bot))