# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands import Greedy

# Other Imports
from datetime import datetime


class Mod_Only(commands.Cog, name="Moderation Commands"):
    """ Moderation related commands """
    def __init__(self, bot):
        self.bot = bot

    @commands.command (
        brief="Kicks a member.",
        description="Kicks a member from the server. Requires the `kick_members` permission.",
        aliases=["k"]
    )
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str=None):
        await member.kick(reason=reason)
        embed = discord.Embed (
            description=f"{member} has been kicked from {ctx.guild.name} for: \n> {reason or 'No reason given.'}",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Action performed by {ctx.author}")
        await ctx.send(embed=embed)
    
    @commands.command (
        brief="Bans a member.",
        description="Bans a member from the server. Requires the `ban_members` permission.",
        aliases=["b"]
    )
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str=None):
        await member.ban(reason=reason)
        embed = discord.Embed (
            description=f"{member} has been banned from {ctx.guild.name} for: \n> {reason or 'No reason given.'}",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Action performed by {ctx.author}")
        await ctx.send(embed=embed)
    
    @commands.command (
        brief="Unbans a member.",
        description="Unbans a member from the server. Requires the `ban_members` permission.",
        aliases=["ub"]
    )
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason: str=None):
        await member.unban(reason=reason)
        embed = discord.Embed (
            description=f"{member} has been unbanned from {ctx.guild.name} for: \n> {reason or 'No reason given.'}",
            color=self.bot.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Action performed by {ctx.author}")
        await ctx.send(embed=embed)
    
    @commands.command (
        brief="Either deletes a certain number of messages or deletes messages until a certain message is reached.",
        description="Giving a number of messages to delete will delete that many messages. Giving a message's id will delete all messages in that message's channel (max of 100 messages) and stop after the given message is deleted. Running the command and not specifying a limit or a message, will send a list of all tags.",
        aliases=["delete", "del", "clear", "cleanup"]
    )
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: Greedy[int], clear_until: Greedy[discord.Message], *, args="--ip"):
        if limit == [] and clear_until == []:
            # Neither is passed, use as a pseudo help command
            args_desc = {
                "--ip": "Ignore pinned messages. (Default)",
                "--ib": "Ignore bot messages.",
                "--content `<text>`": "Will only delete messages that contain the given text."
            }
            embed = discord.Embed (
                description="Here's a list of all possible arguments and what they do.",
                color=self.bot.EMBED_COLOR
            )
            for tag, meaning in args_desc.items():
                embed.add_field (
                    name=tag,
                    value=meaning
                )
            await ctx.send(embed=embed)
            return

        await ctx.message.delete()
        args = [i.strip(" ") for i in args.split("--")[1:]] # get arguments as a list
        deleted_messages = {}
        text_to_clear = None
        if limit:
            async for message in ctx.channel.history(limit=limit[0]):
                delete_message = True
                # Check the message against the given arguments
                if "ip" in args and message.pinned:
                    delete_message = False
                if "ib" in args and message.author.bot:
                    delete_message = False
                if "content" in str(args):
                    for tag in args:
                        if tag.startswith("content"):
                            text_to_clear = tag[len("content "):].lower() # get only the text
                    if text_to_clear not in message.content.lower():
                        delete_message = False
                
                if delete_message:
                    count = deleted_messages.get(message.author, 0)
                    count += 1
                    deleted_messages.update({message.author: count})
                    await message.delete()

        elif clear_until:
            async for message in clear_until[0].channel.history(limit=100):
                count = deleted_messages.get(message.author, 0)
                count += 1
                deleted_messages.update({message.author: count})
                await message.delete()
                if message == clear_until[0]:
                    break
                
        deleted = sum(deleted_messages.values())
        messages = [f"{f'*Only messages containing the phrase `{text_to_clear}` were deleted*' if text_to_clear is not None else ''}\n{deleted} message{' was' if deleted == 1 else 's were'} removed."]
        messages.extend(f"- **{author}**: {count}" for author, count in deleted_messages.items())
        await ctx.send("\n".join(messages), delete_after=10)


def setup(bot):
    bot.add_cog(Mod_Only(bot))