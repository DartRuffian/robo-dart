# Discord Imports
import asyncio

import discord
from discord.ext import commands

# Other Imports
import json
import os


class AnonChannelHandler:
    def __init__(self, bot: commands.Bot, file_dir: str):
        self.bot = bot
        self.file_dir = file_dir
        self._channels: dict[str: list[discord.TextChannel]] = self.load(file_dir)

    @property
    def vent_channels(self) -> dict[str: list[discord.TextChannel]]:
        return self._channels

    def to_json(self) -> dict[str: list[int]]:
        """Returns the self.vent_channels attribute as a json-valid object"""
        json_object: dict[str: list[int]] = {}
        for guild_id, channels in self._channels.items():
            json_object[str(guild_id)] = [channel.id for channel in channels]
        return json_object

    def save(self) -> None:
        """Saves the self.vent_channels attribute to the file path for the given instance"""
        json_object = self.to_json()
        with open(self.file_dir, "w") as f:
            json.dump(json_object, f, indent=2)

    def load(self, file_dir: str = None) -> dict[str: list[discord.TextChannel]]:
        """Loads the given file at the given file path and returns it as a dict of a guild id to a list of channels"""
        if file_dir is None:
            file_dir = self.file_dir
        with open(file_dir, "r") as f:
            saved_anon_data = json.load(f)

        for guild_id, channels in saved_anon_data.items():
            # Convert channel ids to discord.TextChannel objects
            guild = self.bot.get_guild(int(guild_id))
            saved_anon_data[guild_id] = [guild.get_channel(channel) for channel in channels]
        self._channels = saved_anon_data
        return saved_anon_data

    def add_channel(self, channel: discord.TextChannel) -> bool:
        """Adds a given channel to the list of anonymous channels for the channel's guild.
Returns a bool of whether the channel was added or not"""
        self.load()
        channels = self._channels.get(str(channel.guild.id), [])
        if channel not in channels:
            channels.append(channel)
            self._channels.update({str(channel.guild.id): channels})
        self.save()
        return channel in self._channels.get(str(channel.guild.id), [])

    def remove_channel(self, channel: discord.TextChannel) -> bool:
        """Removes a given channel to the list of anonymous channels for the channel's guild.
Returns a bool of whether the channel was removed or not"""
        self.load()
        channels = self._channels.get(str(channel.guild.id), [])
        if channel in channels:
            channels.remove(channel)
            if not channels:
                del self._channels[str(channel.guild.id)]
            else:
                self._channels.update({str(channel.guild.id): channels})
        self.save()
        return channel in self._channels.get(str(channel.guild.id), [])


def create_embed(message: str) -> discord.Embed:
    """Creates an embed with a given message and transparent color (for rounded corners)"""
    embed = discord.Embed(
        description=message,
        color=0x2F3136
    )
    embed.set_footer(text="""Want to talk anonymously? Just DM the bot "!ac" followed by your message.""")
    return embed


class AnonymousConfessions(commands.Cog, name="Anonymous Confessions"):
    """Commands for anonymously discussing topics"""

    def __init__(self, bot):
        self.bot = bot
        self.handler = None  # Temporary value, is updated in the on_ready listener

    @commands.Cog.listener()
    async def on_ready(self):
        self.handler = AnonChannelHandler(self.bot, f"{self.bot.BASE_DIR}/resources/vent_channels.json")

    @commands.command(
        brief="...",
        description="...",
        aliases=["confess", "vent", "ac"]
    )
    @commands.dm_only()
    async def anon_confess(self, ctx, *, message: str):
        def check(m):
            """Checks that a message is from the author and is in the same channel"""
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        guilds = [guild for guild in self.bot.guilds if ctx.author in guild.members]
        guild_names = [f"`{guild.name}`""\n" for guild in guilds]

        while True:
            # Get the guild that the user would like to send the message to
            await ctx.send(f"""Here's a list of common servers between us, please select one to send your message to:
{"".join(guild_names)}

Or if you'd like to cancel your message, type `cancel`.""")

            try:
                chosen_guild = await self.bot.wait_for("message", check=check, timeout=30.0)
                if chosen_guild.content.lower() == "cancel":
                    await ctx.send("Cancelling message...")
                    return

                chosen_guild = discord.utils.get(guilds, name=chosen_guild.content)
                if chosen_guild is not None:
                    break
                else:
                    await ctx.send(f"Couldn't convert value to a server, "
                                   "make sure that the server name is spelled correctly.")
                    continue

            except asyncio.TimeoutError:
                await ctx.send("Your message has timed out, please try again!")
                return
        await ctx.send(f"Selected {chosen_guild.name}!")

        channels = self.handler.vent_channels[str(chosen_guild.id)]
        channel_names = [f"`{channel.name}`""\n" for channel in channels]

        await ctx.send(f"""Your message has been received, where would you like to send it to?
{"".join(channel_names)}
Or if you'd like to cancel your message, type `cancel`.""")
        while True:
            try:
                chosen_channel = await self.bot.wait_for("message", check=check, timeout=30.0)
                if chosen_channel.content.lower() == "cancel":
                    await ctx.send("Cancelling message...")
                    return

                chosen_channel = discord.utils.get(chosen_guild.text_channels, name=chosen_channel.content)
                if chosen_channel is not None:
                    break
                else:
                    await ctx.send(f"Couldn't convert value to a channel, "
                                   "make sure that the channel name is spelled correctly.")
                    continue

            except asyncio.TimeoutError:
                await ctx.send("Your message has timed out, please try again!")
                return

        embed = create_embed(message)
        await chosen_channel.send(embed=embed)

    @commands.group(
        brief="...",
        description="...",
        aliases=["channels"],
        invoke_without_command=True,
    )
    @commands.has_permissions(manage_channels=True)
    async def channel(self, ctx):
        """The base command for the group, which will only send the help page for the group itself (WIP)"""
        listed_channels = self.handler.vent_channels.get(
            str(ctx.guild.id)
        )
        if listed_channels is None:
            # No channels saved for the current server
            await ctx.send(f"""There aren't any channels set up to be anonymous for **{ctx.guild.name}**.
You can add channels using `{ctx.prefix}channel add #channel`, where `#channel` is a channel mention!""")
        else:
            await ctx.send(f"""Here's a list of all anonymous channels for **{ctx.guild.name}**
{"".join([f" • {channel.mention}" for channel in listed_channels])}""")

    @channel.command()
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx, channel: discord.TextChannel):
        self.handler.add_channel(channel)
        await ctx.send(f"{channel.mention} has been added as an anonymous channel! "
                       f"You can view the full list with `{ctx.prefix}channels`")

    @channel.command()
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx, channel: discord.TextChannel):
        self.handler.remove_channel(channel)
        await ctx.send(f"{channel.mention} has been removed from the list of anonymous channels! "
                       f"You can view the full list with `{ctx.prefix}channels`")


def setup(bot):
    bot.add_cog(AnonymousConfessions(bot))
