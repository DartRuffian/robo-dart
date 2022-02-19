# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands import Greedy

# Other Imports
from datetime import datetime


def create_embed(ctx, message) -> discord.Embed:
    embed = discord.Embed(
            description=message,
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
    embed.set_footer(text=f"Action performed by {ctx.author}")
    return embed


class ModOnly(commands.Cog, name="Moderation"):
    """Moderation related commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Kicks a member.",
        description="Kicks a member from the server. Requires the `kick_members` permission.",
        aliases=["k"]
    )
    @has_permissions(kick_members=True)
    async def kick(self, ctx, members: Greedy[discord.Member], *, reason: str = None):
        if not members:
            await ctx.send("Make sure to include at least one member when running the command.")
            return
        [await member.kick(reason=reason) for member in members]
        kicked_members = "".join([f"- {member.mention}\n" for member in members])
        embed = create_embed(
            ctx,
            f"The following members have been kicked from {ctx.guild.name}:"
            f"\n {kicked_members} for: \n> {reason or 'No reason given.'}"
        )
        embed.set_footer(text=f"Action performed by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(
        brief="Bans a member.",
        description="Bans a member from the server. Requires the `ban_members` permission.",
        aliases=["b"]
    )
    @has_permissions(ban_members=True)
    async def ban(self, ctx, members: Greedy[discord.Member], *, reason: str = None):
        if not members:
            await ctx.send("Make sure to include at least one member when running the command.")
            return
        [await member.ban(reason=reason) for member in members]
        banned_members = "".join([f"- {member.mention}\n" for member in members])
        embed = create_embed(
            ctx,
            f"The following members have been banned from {ctx.guild.name}:"
            f"\n {banned_members} for: \n> {reason or 'No reason given.'}"
        )
        await ctx.send(embed=embed)

    @commands.command(
        brief="Unbans a member.",
        description="Unbans a member from the server. Requires the `ban_members` permission.",
        aliases=["ub"]
    )
    @has_permissions(ban_members=True)
    async def unban(self, ctx, members: Greedy[discord.Member], *, reason: str = None):
        if not members:
            await ctx.send("Make sure to include at least one member when running the command.")
            return
        [await member.unban(reason=reason) for member in members]
        unbanned_members = "".join([f"- {member.mention}\n" for member in members])
        embed = create_embed(
            ctx,
            f"The following members have been unbanned from {ctx.guild.name}:"
            f"\n {unbanned_members} for: \n> {reason or 'No reason given.'}"
        )
        await ctx.send(embed=embed)

    @commands.command(
        brief="Either deletes a certain number of messages or deletes messages until a certain message is reached.",
        description="Giving a number of messages to delete will delete that many messages. "
                    "Giving a message's id will delete all messages in that message's channel (max of 100 messages) "
                    "and stop after the given message is deleted. Running the command and not specifying a limit or a "
                    "message, will send a list of all tags.",
        aliases=["delete", "del", "clear", "cleanup"]
    )
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: Greedy[int], clear_until: Greedy[discord.Message] = None):
        await ctx.message.delete()

        if limit:
            await ctx.channel.purge(limit=limit[0])

        elif clear_until:
            async for message in clear_until[0].channel.history(limit=100):
                await message.delete()
                if message == clear_until[0]:
                    break


def setup(bot):
    bot.add_cog(ModOnly(bot))
