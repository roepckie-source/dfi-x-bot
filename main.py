import os
import tweepy
import requests
from datetime import datetime


# X API Daten
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


# -------------------------
# DFI Kurs holen
# -------------------------

def get_dfi_price():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "defichain",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    r = requests.get(url, params=params)
    data = r.json()

    price = data["defichain"]["usd"]
    change = data["defichain"]["usd_24h_change"]

    return price, change


# -------------------------
# X Verbindung
# -------------------------

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)


# Test Verbindung

try:
    me = client.get_me()
    print("X Verbindung erfolgreich")
    print(me.data.username)

except Exception as e:
    print("Fehler bei der X-Verbindung:", e)


# -------------------------
# Tweet erstellen
# -------------------------

try:

    price, change = get_dfi_price()

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    tweet = f"""
🚀 DFI Daily Update

💰 Price: ${price:.5f}
📈 24h Change: {change:.2f}%

🕒 {now}

#DeFiChain #DFI
"""

    response = client.create_tweet(
        text=tweet
    )

    print("Tweet erfolgreich gesendet")


except Exception as e:
    print("Fehler beim Tweet:", e)


# -------------------------
# Discord Nachricht
# -------------------------

try:

    message = {
        "content":
        "✅ DFI Bot ausgeführt\n\n" + tweet
    }

    requests.post(
        DISCORD_WEBHOOK,
        json=message
    )

    print("Discord Nachricht erfolgreich gesendet")

except Exception as e:
    print("Discord Fehler:", e)
