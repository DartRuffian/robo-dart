# Discord Imports
import discord
from discord.ext import commands


class Hub_Only(commands.Cog):
    """Emoji Hub Only Commands/Listeners"""
    def __init__(self, bot):
        self.bot = bot
    
    def reload_emojis(self):
        """Load all custom emojis from the Emoji Hub server to a dictionary"""
        self.bot.cust_emojis = {emoji.name: emoji for emoji in self.bot.get_guild(903452394204065833).emojis}

    @commands.Cog.listener()
    async def on_ready(self):
        self.reload_emojis()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clone_all_emojis(self, ctx, guild: discord.Guild):
        await ctx.send("Copying emojis... this may take a while")
        async with ctx.channel.typing():
            copied_emojis = [await ctx.guild.create_custom_emoji(name=emoji.name, image=await emoji.url.read()) for emoji in guild.emojis]
            
            await ctx.send("Copied Emojis:\n" + " ".join([str(emoji) for emoji in copied_emojis]))
            self.reload_emojis()

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if guild.id != 903452394204065833 or len(before) > len(after):
            return
        self.reload_emojis()
        channel = guild.get_channel(903453089128919151)
        if len(after) > len(before):
            await channel.send(f"{after[-1]} -- `{after[-1]}`")


def setup(bot):
    bot.add_cog(Hub_Only(bot))
