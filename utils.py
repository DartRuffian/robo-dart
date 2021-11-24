# Discord Imports
import discord

# Other Imports
from wikipediaapi import WikipediaPage
import os


class Utils:
    def __init__(self, bot: discord.ext.commands.Bot):
        self._bot = bot

    def log(self, message: str) -> None:
        os.chdir(f"{self._bot.BASE_DIR}/resources")
        with open("bot.log", "a") as f:
            f.write(message + "\n\n")
        os.chdir(self._bot.BASE_DIR)

    def embed_from_wiki_page(self, page: WikipediaPage) -> discord.Embed:
        embed = discord.Embed(
            description=page.summary.split("\n")[0],
            color=self._bot.EMBED_COLOR
        )
        embed.set_author(name=f"{page.title} (Click for Full Page)", url=page.fullurl)
        return embed
