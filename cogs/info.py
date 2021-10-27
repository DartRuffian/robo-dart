# Discord Imports
import discord
from discord.channel import DMChannel
from discord.ext import commands

# Uptime Imports
from datetime import datetime


class Bot_Info(commands.Cog, name="Information"):
    """ Bot and Author Info """
    def __init__(self, bot):
        self.bot = bot
    
    def timestamp(self, time, mode="F"):
        return f"<t:{str(time.timestamp()).split('.')[0]}:{mode}>"

    
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
        description="Gives some basic infomration of the bot's author: DartRuffian.",
        aliases=["author"]
    )
    async def author_info(self, ctx):
        author = self.bot.get_user(self.bot.owner_id)
        author_info = {
            "Name": {"text": author.name, "inline": True},
            "Discord Account": {"text": author, "inline": True},
            "Discord ID": {"text": f"`{author.id}`", "inline": True},
            "Account Created At": {"text": f"{self.timestamp(author.created_at)}\n{self.timestamp(author.created_at, 'R')}", "inline": True},
            "About Me": {"text": f"Hey there! First off I'd like to thank you for using my bot, {self.bot.user.name}. I'm an aspiring Software Engineer who specializes in primarily Python.", "inline": False},
            "Connected Accounts": {"text": f"[Github](https://github.com/{author.name}/ 'View {author.name} on Github')\n[Spotify](https://open.spotify.com/user/w8hah1vw86ysdslahmv5fsm9b/ 'View {author.name} on Spotify')\n[Steam](https://steamcommunity.com/id/{author.name}/ 'View {author.name} on Steam')", "inline": False}
        }

        embed = discord.Embed(color=self.bot.EMBED_COLOR)
        for k, v in author_info.items():
            embed.add_field(name=k, value=v["text"], inline=v.get("inline", True))

        embed.set_thumbnail(url=author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command (
        brief="The generic version of `author_info`.",
        description="The generic version of `author_info`, does not include connected accounts.",
        aliases=["userinfo", "ui"]
    )
    @commands.guild_only()
    async def user_info(self, ctx, user: discord.Member=None):
        start_time = datetime.utcnow()
        async with ctx.channel.typing():
            user = user or ctx.author # Get the user's profile if no member is passed
            status_dict = {
                discord.Status.online: self.bot.cust_emojis["status_online"],
                discord.Status.idle: self.bot.cust_emojis["status_idle"],
                discord.Status.dnd: self.bot.cust_emojis["status_dnd"],
                discord.Status.offline: self.bot.cust_emojis["status_offline"],
            }
            user_info = {
                "Account Info": [
                    f"{self.bot.cust_emojis['name_tag']} Username: {user}",
                    f"{self.bot.cust_emojis['green_tick'] if user.nick is not None else self.bot.cust_emojis['gray_tick']} Nickname: {user.nick or 'No Nickname Set'}",
                    f"{self.bot.cust_emojis['profile']} Profile Picture: [URL]({user.avatar_url} \"{user.name}'s Profile Picture\")",
                    f"{self.bot.cust_emojis['authorized']} ID: {user.id}",
                    f"{self.bot.cust_emojis['bot_tag']} Bot Account: {self.bot.cust_emojis['green_tick'] if user.bot else self.bot.cust_emojis['red_tick']}",
                    f"{self.bot.cust_emojis['settings']} Created At: {self.timestamp(user.created_at)} - {self.timestamp(user.created_at, 'R')}",
                ],
                "Server Info": [
                    f"{self.bot.cust_emojis['member_join']} Joined At: {self.timestamp(user.joined_at)} - {self.timestamp(user.joined_at, 'R')}",
                    f"{self.bot.cust_emojis['owner']} Server Owner: {self.bot.cust_emojis['green_tick'] if user == ctx.guild.owner else self.bot.cust_emojis['red_tick']}",
                    f"{self.bot.cust_emojis['booster']} Server Booster: {self.bot.cust_emojis['green_tick'] if user in ctx.guild.premium_subscribers else self.bot.cust_emojis['red_tick']}",
                    f"{self.bot.cust_emojis['mention']} Top Role: {user.top_role.mention}"
                ],
                "Status Info": [
                    f"🖥️ Desktop: {status_dict[user.desktop_status]}",
                    f"🕸️ Web: {status_dict[user.web_status]}",
                    f"📱 Mobile: {status_dict[user.mobile_status]}",
                ]
            }
            user_embed = discord.Embed(color=self.bot.EMBED_COLOR, timestamp=datetime.utcnow())
            user_embed.set_thumbnail(url=user.avatar_url)
            for section_title, section_info in user_info.items():
                user_embed.add_field(name=section_title, value="\n".join(section_info), inline=False)
            user_embed.set_footer(text=f"Finished in: {round((datetime.utcnow() - start_time).total_seconds(), 2)} seconds.")
            await ctx.send(embed=user_embed)
    
    @commands.command (
        brief="Returns the bot's prefixes.",
        description="Returns all available prefixes of the bot for the current guild.",
        aliases=["prefixes"]
    )
    async def prefix(self, ctx):
        # if '<' not in prefix and '>' not in prefix else prefix for prefix in await self.bot.get_prefix(ctx.message)
        # will place backticks at the begining and ending of entries from get_prefix() that do not contain both angle brackets.
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