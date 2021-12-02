# Discord Imports
import discord
from discord.ext import commands

# Streaming Imports
import youtube_dl


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""

    @classmethod
    async def from_url(cls, ytdl, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        filename = data["title"] if stream else ytdl.prepare_filename(data)
        return filename


async def connect(ctx) -> bool:
    """Returns whether the bot connected to a voice channel"""
    # TODO: Rewrite this to use a before_invoke wrapper
    if not ctx.message.author.voice:
        # User is not connected to a voice channel
        await ctx.send("Whoops! I got lost on the way to your voice channel, could you try joining one first?")
        return False

    channel = ctx.message.author.voice.channel
    await channel.connect()
    return True


async def disconnect(ctx) -> bool:
    """Returns whether the bot disconnected from a voice channel"""
    # TODO: Rewrite this to use a before_invoke wrapper
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        return True
    else:
        await ctx.send("I'm not currently in a voice channel, did you mean to have me join one?")
        return False


def setup_ytdl():
    youtube_dl.utils.bug_reports_message = lambda: ""
    ytdl_format_options = {
        "format": "bestaudio/best",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0"  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }
    ffmpeg_options = {
        "options": "-vn"
    }
    return youtube_dl.YoutubeDL(ytdl_format_options)


class MusicPlayer(commands.Cog, name="Panic at the Voice Channel"):
    """"""
    def __init__(self, bot):
        self.bot = bot
        self.ytdl = setup_ytdl()

    @commands.command(
        brief="Plays a given Youtube url.",
        description="Takes a Youtube url and plays it to the voice channel that the user is in.",
        aliases=["p"]
    )
    async def play(self, ctx, url: str = None):
        if url is None:
            url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            # If no url is given, use Rick Astley's "Never Going to Give You Up" as the default

        if not await connect(ctx):
            return

        temp_message = await ctx.send("Downloading song, this may take a second...")
        async with ctx.channel.typing():
            filename = await YTDLSource.from_url(self.ytdl, url, loop=self.bot.loop)
            await temp_message.delete()
            ctx.message.guild.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            display_name = filename.replace("_", " ")[:-17]  # Remove the youtube id and file extension
            display_name = "".join(display_name)
            await ctx.send(f"**Now Playing:** {display_name}")

    @commands.command(
        brief="Makes the bot leave the voice channel.",
        description="Disconnects the bot from the current voice channel.",
        aliases=["l", "dc", "disconnect"],
    )
    async def leave(self, ctx):
        if await disconnect(ctx):
            await ctx.send("Dipping out!")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
