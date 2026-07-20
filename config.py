import os


# ==============================
# DISCORD
# ==============================

DISCORD_WEBHOOK = os.environ.get(
    "DISCORD_WEBHOOK"
)


# ==============================
# X / TWITTER
# ==============================

API_KEY = os.environ.get(
    "API_KEY"
)

API_SECRET = os.environ.get(
    "API_SECRET"
)

ACCESS_TOKEN = os.environ.get(
    "ACCESS_TOKEN"
)

ACCESS_TOKEN_SECRET = os.environ.get(
    "ACCESS_TOKEN_SECRET"
)


# ==============================
# COINMARKETCAP (später)
# ==============================

CMC_API_KEY = os.environ.get(
    "CMC_API_KEY"
)


# ==============================
# EINSTELLUNGEN
# ==============================

BOT_NAME = "DeFiChain Daily Bot"

VERSION = "2.0"
