import os
import tweepy
import requests
from datetime import datetime


# =========================
# Secrets
# =========================

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


# =========================
# DFI Daten holen
# =========================

def get_crypto_data():

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "defichain,defichain-dusd",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    data = response.json()

    dfi = data.get("defichain", {})

    price = dfi.get("usd", 0)
    change = dfi.get("usd_24h_change", 0)
    marketcap = dfi.get("usd_market_cap", 0)

    dusd = data.get("defichain-dusd", {}).get("usd", 0)

    return price, change, marketcap, dusd


# =========================
# X Verbindung
# =========================

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)


try:
    me = client.get_me()

    print("X Verbindung erfolgreich")
    print(me.data.username)

except Exception as e:
    print("Fehler bei der X-Verbindung:", e)


# =========================
# Report erstellen
# =========================

tweet = ""

try:

    price, change, marketcap, dusd = get_crypto_data()

    marketcap_m = marketcap / 1_000_000

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    if change >= 0:
        trend = "📈"
    else:
        trend = "📉"


    tweet = f"""
📰 DeFiChain Daily Report

📅 {now}

💰 Market Data

DFI Price:
${price:.5f}

24h Change:
{trend} {change:.2f}%

Market Cap:
${marketcap_m:.2f} Mio.

💵 DUSD:
${dusd:.4f}


🌐 Network

DeFiChain ecosystem update


📌 Governance

No new updates detected


#DeFiChain #DFI
"""


    client.create_tweet(
        text=tweet
    )

    print("Tweet erfolgreich gesendet")


except Exception as e:

    print("Fehler beim Tweet:", e)


# =========================
# Discord
# =========================

try:

    requests.post(
        DISCORD_WEBHOOK,
        json={
            "content": "✅ DFI Bot ausgeführt\n\n" + tweet
        },
        timeout=10
    )

    print("Discord Nachricht erfolgreich gesendet")


except Exception as e:

    print("Discord Fehler:", e)
