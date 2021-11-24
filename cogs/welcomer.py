# Discord Imports
import discord
from discord.ext import commands
from discord.utils import get


def create_embed(message, thumbnail_url, color) -> discord.Embed:
    """Creates an embed with a given message, color, and thumbnail"""
    embed = discord.Embed(
        description=message,
        color=color
    )
    embed.set_thumbnail(url=thumbnail_url)
    return embed


class AutoWelcomer(commands.Cog):
    """Auto Welcomer"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = get(member.guild.channels, name="welcome")
        if welcome_channel is not None:
            welcome_embed = create_embed(f"Everyone please welcome {member.mention} to {member.guild.name}!",
                                         member.avatar_url,
                                         0x1dfd00)
            welcome_embed.set_footer(text=f"Member Count: {member.guild.member_count}")
            await welcome_channel.send(embed=welcome_embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome_channel = get(member.guild.channels, name="welcome")
        if welcome_channel is not None:
            welcome_embed = create_embed(f"Sorry to see you go {member.mention}, hope to see you again!",
                                         member.avatar_url,
                                         0xFF0000)
            welcome_embed.set_footer(text=f"Member Count: {member.guild.member_count}")
            await welcome_channel.send(embed=welcome_embed)


def setup(bot):
    bot.add_cog(AutoWelcomer(bot))
