# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands import Greedy

# Other Imports
from datetime import datetime


def check_message(message, tags) -> bool:
    should_delete = True
    # Check the message against the given arguments
    if "ip" in tags and message.pinned:
        should_delete = False
    if "ib" in tags and message.author.bot:
        should_delete = False
    if "content" in str(tags):
        text_to_clear = get_content_tag(tags)
        if text_to_clear not in message.content.lower():
            should_delete = False
    return should_delete


def get_content_tag(tags) -> str:
    for tag in tags:
        if tag.startswith("content"):
            return tag[len("content "):].lower()  # get only the text


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
        embed = discord.Embed(
            description=f"The following members have been banned from {ctx.guild.name}:"
                        f"\n{kicked_members} for: \n> {reason or 'No reason given.'}",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
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
        embed = discord.Embed(
            description=f"The following members have been banned from {ctx.guild.name}:"
                        f"\n{banned_members} for: \n> {reason or 'No reason given.'}",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Action performed by {ctx.author}")
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
        embed = discord.Embed(
            description=f"The following members have been unbanned from {ctx.guild.name}:"
                        f"\n {unbanned_members} for: \n> {reason or 'No reason given.'}",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Action performed by {ctx.author}")
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
    async def purge(self, ctx, limit: Greedy[int], clear_until: Greedy[discord.Message], *, tags=None):
        if tags is None:
            tags = "--ip"

        if limit == [] and clear_until == []:
            # Neither is passed, use as a pseudo help command
            args_desc = {
                "--ip": "Ignore pinned messages. (Default)",
                "--ib": "Ignore bot messages.",
                "--content `<text>`": "Will only delete messages that contain the given text."
            }
            embed = discord.Embed(
                description="Here's a list of all possible arguments and what they do.",
                color=self.bot.EMBED_COLOR
            )
            for tag, meaning in args_desc.items():
                embed.add_field(
                    name=tag,
                    value=meaning
                )
            await ctx.send(embed=embed)
            return

        await ctx.message.delete()
        tags = [i.strip(" ") for i in tags.strip().split("--")]  # get arguments as a list
        deleted_messages = {}
        if limit:
            async for message in ctx.channel.history(limit=limit[0]):
                delete_message = check_message(message, tags)

                if delete_message:
                    count = deleted_messages.get(message.author, 0)
                    count += 1
                    deleted_messages.update({message.author: count})
                    await message.delete()

        elif clear_until:
            async for message in clear_until[0].channel.history(limit=100):
                delete_message = check_message(message, tags)
                if delete_message:
                    count = deleted_messages.get(message.author, 0)
                    count += 1
                    deleted_messages.update({message.author: count})
                    await message.delete()
                    if message == clear_until[0]:
                        break

        deleted = sum(deleted_messages.values())
        messages = [f"{deleted} message{' was' if deleted == 1 else 's were'} removed."]
        messages.extend(f"- **{author}**: {count}" for author, count in deleted_messages.items())
        await ctx.send("\n".join(messages), delete_after=10)


def setup(bot):
    bot.add_cog(ModOnly(bot))
