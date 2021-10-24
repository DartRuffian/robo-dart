""" Main Bot File """
# Discord Imports
import discord
from discord.ext import commands

# Keep Bot Online
from webserver import keep_alive

# Other Imports
from datetime import datetime           # Get bot launch time
from os import listdir, getcwd, environ # Load cogs/environment vars (token)

# Define the bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot (
    command_prefix=commands.when_mentioned_or("!"),
    owner_id=400337254989430784,
    case_insensitive=True,
    intents=intents,
)

# Custom Attributes
bot.BASE_DIR = getcwd()
bot.EMBED_COLOR = 0x0E151D
bot.launch_time = datetime.utcnow()


# Events
@bot.event
async def on_ready():
    # Called whenever the bot connects to Discord
    print("Logged in")
    print(f"Username: {bot.user.name}")
    print(f"User Id : {bot.user.id}")

# Load all cogs
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


# Launch the Bot
keep_alive() # Keep bot running

# Load token
try:
    # If running locally
    with open("token.txt", "r") as f:
        TOKEN = f.read().split("\n")[0]
except FileNotFoundError:
    # If running on server
    TOKEN = environ.get("DISCORD_BOT_SECRET") 

bot.run(TOKEN)