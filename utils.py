# Discord Imports
import discord

# Other Imports
import os


class Utils:
    def __init__(self, bot: discord.ext.commands.Bot):
        self._bot = bot

    def log(self, message: str) -> None:
        os.chdir(f"{self._bot.BASE_DIR}/resources")
        with open("bot.log", "a") as f:
            f.write(message + "\n\n")
        os.chdir(self._bot.BASE_DIR)
