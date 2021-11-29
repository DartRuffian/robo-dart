# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from bs4 import BeautifulSoup
import requests
import os


def cleanup_url(url: str = None) -> str:
    if url is None:
        return "https://en.wikipedia.org/wiki/Special:Random"

    url = url.lower()
    url = " ".join(elem.capitalize() for elem in url.split())
    url = url.replace(" ", "_")
    return f"https://en.wikipedia.org/wiki/{url}"


class WikiTools(commands.Cog, name="Wikipedia Tools"):
    """A set of commands relating to Wikipedia"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        brief="Group of commands relating to Wikipedia articles.",
        description="Group of commands relating to Wikipedia articles, such as searching.",
        aliases=["w"],
        invoke_without_command=True
    )
    async def wiki(self, ctx):
        """Base command, serves only to group commands together"""

    @wiki.command(
        brief="Takes a given search query and looks for a Wikipedia page with that name.",
        description="Takes a given search query and looks for a Wikipedia page with that name.",
        aliases=["s"]
    )
    async def search(self, ctx, *, url: str = None):
        url = cleanup_url(url)

        response = requests.get(url=url)
        if response.status_code == 404:
            await ctx.send(f"""Sorry, but it doesn't seem like {url} is a page that exists.
Double check your spelling and try again, capitalization and spaces do not matter.""")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        all_paragraphs = soup.find_all("p")
        summary = [p.get_text() for p in all_paragraphs if p.get_text() != "\n"].pop()
        image = soup.find_all("img")[0].get("src")

        embed = discord.Embed(
            description=summary,
            color=self.bot.EMBED_COLOR
        )
        embed.set_image(url="https:" + image)
        embed.set_author(name=f"{soup.find(id='firstHeading').string} (Click for Full Page)", url=url)
        await ctx.send(embed=embed)

    @wiki.command(
        brief="Saves an entire Wikipedia article as a `.txt` file.",
        description="Takes a link to a Wikipedia page and saves it to a `.txt` file."
    )
    async def save(self, ctx, url: str):
        url = url.replace("https://en.wikipedia.org/wiki/", "")
        url = cleanup_url(url)

        response = requests.get(url=url)
        if response.status_code == 404:
            await ctx.send(f"""Sorry, but it doesn't seem like {url} is a page that exists.
Double check your spelling and try again, capitalization and spaces do not matter.""")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        all_paragraphs = [text.get_text() for text in soup.find_all("p") if text.get_text() != "\n"]
        title = soup.find(id='firstHeading').string.lower().replace(" ", "_")

        async with ctx.channel.typing():
            os.chdir(f"{self.bot.BASE_DIR}/resources")
            with open("latest_article.txt", "w", encoding="utf-8") as f:
                f.write("".join(all_paragraphs))
            with open("latest_article.txt", "rb") as f:
                await ctx.send(
                    f"Saved all available text for the article at: <{url}>.",
                    file=discord.File(f, f"{title}.txt")
                )
            os.chdir(self.bot.BASE_DIR)


def setup(bot):
    bot.add_cog(WikiTools(bot))
