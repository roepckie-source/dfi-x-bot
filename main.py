import os
import requests
import tweepy
import json
from datetime import datetime


# Discord
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# X
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


# DFI + DUSD Daten von CoinGecko holen
def get_dfi_data():

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "defichain,decentralized-usd",
        "vs_currencies": "usd,eur",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    dfi = data["defichain"]
    dusd = data["decentralized-usd"]

    return {

        # DFI
        "usd": dfi["usd"],
        "eur": dfi["eur"],
        "change": dfi["usd_24h_change"],

        # DUSD
        "dusd_usd": dusd["usd"],
        "dusd_eur": dusd["eur"],
        "dusd_change": dusd["usd_24h_change"]
    }



# DeFiChain News laden
def get_dfi_news():

    try:

        with open("dfi_news.json", "r", encoding="utf-8") as file:
            news = json.load(file)

        day = datetime.now().timetuple().tm_yday

        index = (day - 1) % len(news)

        return news[index]


    except Exception as e:

        print("News Fehler:")
        print(e)

        return {
            "title": "Keine News verfügbar",
            "text": "DeFiChain Daily Update",
            "hashtags": "#DeFiChain"
        }



# Discord senden
def send_discord(message):

    try:

        response = requests.post(
            DISCORD_WEBHOOK,
            json={"content": message}
        )

        if response.status_code == 204:
            print("Discord Nachricht erfolgreich gesendet")
        else:
            print(response.text)

    except Exception as e:
        print("Discord Fehler:", e)



# X senden
def send_x(message):

    try:

        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        response = client.create_tweet(text=message)

        print("X Tweet erfolgreich gesendet")
        print(response)


    except Exception as e:

        print("X Fehler:", e)



# Hauptprogramm
try:

    dfi = get_dfi_data()

    news = get_dfi_news()

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    change = dfi["change"]

    emoji = "🟢" if change >= 0 else "🔴"


    warning = ""

    if abs(change) > 20:

        warning = (
            "\n⚠️ Extreme Bewegung erkannt!\n"
            "Bitte Daten prüfen.\n"
        )



    # Discord Nachricht

    discord_message = f"""
🚀 **DeFiChain DFI Update**

💰 **DFI Preis**

🇺🇸 USD: ${dfi['usd']:.6f}
🇪🇺 EUR: €{dfi['eur']:.6f}

{emoji} **24h Änderung:** {change:.2f}%


💵 **DUSD Preis**

🇺🇸 USD: ${dfi['dusd_usd']:.4f}
🇪🇺 EUR: €{dfi['dusd_eur']:.4f}

📊 **DUSD 24h:** {dfi['dusd_change']:.2f}%


📈 **24h Hoch**
${dfi.get('high', 0):.6f}

📉 **24h Tief**
${dfi.get('low', 0):.6f}

💧 **Volumen 24h**
${dfi.get('volume', 0):,.0f}


{warning}


📚 **DeFiChain Daily News**

📰 **{news['title']}**

{news['text']}

{news['hashtags']}


🕒 {now}

🔗 https://defichain.com
"""


    # X Nachricht

    x_message = (
        f"🚀 DeFiChain $DFI Daily Update\n\n"
        f"💰 DFI Price:\n"
        f"🇺🇸 ${dfi['usd']:.6f}\n"
        f"🇪🇺 €{dfi['eur']:.6f}\n\n"
        f"📊 24h: {emoji} {change:.2f}%\n\n"
        f"💵 DUSD:\n"
        f"${dfi['dusd_usd']:.4f}\n\n"
        f"#DeFiChain #DFI #DUSD"
    )



    send_discord(discord_message)

    send_x(x_message)



except Exception as e:

    print("Fehler:")
    print


