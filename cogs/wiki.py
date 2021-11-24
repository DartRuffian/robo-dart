# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import wikipediaapi  # https://pypi.org/project/Wikipedia-API/
from utils import Utils
import os


class WikiTools(commands.Cog, name="Wikipedia Tools"):
    """A set of commands relating to Wikipedia"""
    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipediaapi.Wikipedia("en")

    @commands.group(
        brief="Group of commands relating to Wikipedia articles.",
        description="Group of commands relating to Wikipedia articles, such as searching.",
        aliases=["w"],
        invoke_without_command=True
    )
    async def wiki(self, ctx, *args):
        """Base command, serves only to group commands together"""

    @wiki.command(
        brief="Takes a given search query and looks for a Wikipedia page with that name.",
        description="Takes a given search query and looks for a Wikipedia page with that name.",
        aliases=["s"]
    )
    async def search(self, ctx, *, term: str):
        term = term.lower().replace(" ", "_")
        page = self.wiki.page(term)

        if not page.exists():
            await ctx.send(f"There were no articles with the name of `{term}`, please try again.")
            return

        await ctx.send(embed=self.bot.utils.embed_from_wiki_page(page))

    @wiki.command(
        brief="Saves an entire Wikipedia article as a `.txt` file.",
        description="Takes a link to a Wikipedia page and saves it to a `.txt` file."
    )
    async def save(self, ctx, url: str):
        term = url.replace("https://en.wikipedia.org/wiki/", "")
        page = self.wiki.page(term)

        if not page.exists():
            await ctx.send(f"There were no articles with the name of `{term}`, please try again.")
            return

        async with ctx.channel.typing():
            os.chdir(f"{self.bot.BASE_DIR}/resources")
            with open("latest_article.txt", "w", encoding="utf-8") as f:
                f.write(page.text)
            with open("latest_article.txt", "rb") as f:
                await ctx.send(
                    f"Saved all available text for the article at: <{url}>.",
                    file=discord.File(f, f"{page.title}.txt")
                )
            os.chdir(self.bot.BASE_DIR)


def setup(bot):
    bot.add_cog(WikiTools(bot))
