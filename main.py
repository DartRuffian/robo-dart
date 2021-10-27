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
intents.presences = True
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
bot.cust_emojis = {
    "status_online"   : "<:status_online:902734042552737832>",
    "status_idle"     : "<:status_idle:902734068532260864>",
    "status_dnd"      : "<:status_dnd:902734083950534656>",
    "status_offline"  : "<:status_offline:902734093970718770>",
    "status_streaming": "<:status_streaming:902734109128949820>",
    "green_tick"      : "<:green_tick:902733973162197034>",
    "red_tick"        : "<:red_tick:902733992762155008>",
    "gray_tick"       : "<:gray_tick:902734001859620886>",
    "member_join"     : "<:member_join:902734371814010940>",
    "bot_tag"         : "<:bot_tag:902734116271849512>",
    "github"          : "<:github:902733789007061072>",
    "mention"         : "<:mention:902737646135160862>",
    "name_tag"        : "<:name_tag:902737654066597898>",
    "settings"        : "<:settings:902737667823919114>",
    "authorized"      : "<:authorized:902737626606501901>",
    "profile"         : "<:profile:902756105074135052>",
    "owner"           : "<:owner:902757689409568840>",
    "booster"         : "<:booster:902757697164816394>",
}


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