import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Telegram API configuration
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_USERNAME = getenv("OWNER_USERNAME", "karan")
BOT_USERNAME = getenv("BOT_USERNAME", "Nezuko_RoxBot")
BOT_NAME = getenv("BOT_NAME", "Nezuko")

# MongoDB configuration
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Git configuration
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/ProGamer097/NezukoBot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")  # Default to 'main'
GIT_TOKEN = getenv("GIT_TOKEN", None)

# Additional configurations
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
LOGGER_ID = int(getenv("LOGGER_ID", -1001836376079))
OWNER_ID = int(getenv("OWNER_ID", 6965147961))

# Support links
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/naruto_support1")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/naruto_support1")

# Validate URLs
if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL URL is invalid. It must start with 'https://'")
if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT URL is invalid. It must start with 'https://'")

# Convert time limit to seconds
def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))


DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")
