import os
import requests
import tweepy
from datetime import datetime


# Discord Webhook aus GitHub Secrets laden
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


# X (Twitter) Zugangsdaten aus GitHub Secrets laden
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


# DFI Preis von CoinGecko abrufen
def get_dfi_price():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "defichain",
        "vs_currencies": "usd,eur",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    dfi = data["defichain"]

    return (
        dfi["usd"],
        dfi["eur"],
        dfi.get("usd_24h_change", 0)
    )


# Discord Nachricht senden
def send_discord(message):
    try:
        response = requests.post(
            DISCORD_WEBHOOK,
            json={
                "content": message
            }
        )

        if response.status_code == 204:
            print("Discord Nachricht erfolgreich gesendet")
        else:
            print("Discord Fehler:")
            print(response.text)

    except Exception as e:
        print("Discord Fehler:")
        print(e)


# Nachricht auf X posten
def send_x(message):
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        response = client.create_tweet(
            text=message
        )

        print("X Tweet erfolgreich gesendet")
        print(response)

    except Exception as e:
        print("X Fehler:")
        print(e)


# Hauptprogramm
try:

    dfi_usd, dfi_eur, change = get_dfi_price()

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    emoji = "🟢" if change >= 0 else "🔴"


    # Discord Nachricht
    discord_message = f"""
🚀 **DeFiChain DFI Update**

💰 **DFI Preis**

🇺🇸 USD: ${dfi_usd:.6f}
🇪🇺 EUR: €{dfi_eur:.6f}

{emoji} **24h Änderung:** {change:.2f}%

🕒 Zeit:
{now}

🔗 https://defichain.com
"""


    # X Nachricht optimiert
    x_message = (
        f"🚀 DeFiChain $DFI Daily Update\n\n"
        f"💰 Price:\n"
        f"🇺🇸 ${dfi_usd:.6f}\n"
        f"🇪🇺 €{dfi_eur:.6f}\n\n"
        f"📊 24h Change:\n"
        f"{emoji} {change:.2f}%\n\n"
        f"🕒 {now} UTC\n\n"
        f"#DeFiChain #DFI #Crypto"
    )


    # Beide Plattformen senden
    send_discord(discord_message)
    send_x(x_message)


except Exception as e:
    print("Fehler:")
    print(e)
