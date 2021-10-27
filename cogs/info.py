# Discord Imports
import discord
from discord.ext import commands

# Uptime Imports
from datetime import datetime


class Bot_Info(commands.Cog, name="Information"):
    """ Bot and Author Info """
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command (
        brief="Returns how long the bot has been online for.",
        description="Returns how much time has passed since the bot last booted."
    )
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_embed = discord.Embed (
            description=f"Uptime: `{days}d, {hours}h, {minutes}m, {seconds}s`",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=uptime_embed)
    
    @commands.command (
        brief="Gives some basic info of the bot author.",
        description="Gives some basic infomration of the bot's author: DartRuffian",
        aliases=["author"]
    )
    async def author_info(self, ctx):
        author = self.bot.get_user(self.bot.owner_id)
        author_info = {
            "Name": {"text": author.name, "inline": True},
            "Discord Account": {"text": author, "inline": True},
            "Discord ID": {"text": f"`{author.id}`", "inline": True},
            "Account Created At (UTC)": {"text": author.created_at, "inline": True},
            "About Me": {"text": f"Hey there! First off I'd like to thank you for using my bot, {self.bot.user.name}. I'm an aspiring Software Engineer who specializes in primarily Python.", "inline": False},
            "Connected Accounts": {"text": f"[Github](https://github.com/{author.name}/ 'View {author.name} on Github')\n[Spotify](https://open.spotify.com/user/w8hah1vw86ysdslahmv5fsm9b/ 'View {author.name} on Spotify')\n[Steam](https://steamcommunity.com/id/{author.name}/ 'View {author.name} on Steam')", "inline": False}
        }

        embed = discord.Embed(color=self.bot.EMBED_COLOR)
        for k, v in author_info.items():
            embed.add_field(name=k, value=v["text"], inline=v.get("inline", True))

        embed.set_thumbnail(url=author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command (
        brief="Returns the bot's prefix.",
        description="Returns the bot's prefix for the current guild.",
        aliases=["prefixes"]
    )
    async def prefix(self, ctx):
        # if '<' not in prefix and '>' not in prefix else prefix for prefix in await self.bot.get_prefix(ctx.message) will place backticks at the begining and ending of
        # entries from get_prefix() that do not contain both angle brackets.
        # That way, only "normal" prefixes will be placed into single line code formatting, while mentions remain readable.
        embed = discord.Embed (
            title="__Prefix List:__",
            description="\n".join([f'• `{prefix}`' if '<' not in prefix and '>' not in prefix else f'• {prefix}' for prefix in await self.bot.get_prefix(ctx.message)]),
            color=self.bot.EMBED_COLOR
        )
        #embed.set_footer(text=f"These prefixes are only for {ctx.guild.name}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Bot_Info(bot))