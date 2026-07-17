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


# DFI Daten von CoinGecko holen
def get_dfi_data():

    url = "https://api.coingecko.com/api/v3/coins/defichain"

    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    market = data["market_data"]

    return {
        "usd": market["current_price"]["usd"],
        "eur": market["current_price"]["eur"],
        "change": market["price_change_percentage_24h"],
        "high": market["high_24h"]["usd"],
        "low": market["low_24h"]["usd"],
        "volume": market["total_volume"]["usd"]
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



    # Discord mit News

    discord_message = f"""
🚀 **DeFiChain DFI Update**

💰 **Preis**

🇺🇸 USD: ${dfi['usd']:.6f}
🇪🇺 EUR: €{dfi['eur']:.6f}

{emoji} **24h Änderung:** {change:.2f}%


📈 **24h Hoch**
${dfi['high']:.6f}

📉 **24h Tief**
${dfi['low']:.6f}

💧 **Volumen 24h**
${dfi['volume']:,.0f}

{warning}


📚 **DeFiChain Daily News**

📰 **{news['title']}**

{news['text']}

{news['hashtags']}


🕒 {now}

🔗 https://defichain.com
"""



    # X bleibt bewusst unverändert

    x_message = (
        f"🚀 DeFiChain $DFI Daily Update\n\n"
        f"💰 Price:\n"
        f"🇺🇸 ${dfi['usd']:.6f}\n"
        f"🇪🇺 €{dfi['eur']:.6f}\n\n"
        f"📊 24h:\n"
        f"{emoji} {change:.2f}%\n\n"
        f"📈 High: ${dfi['high']:.6f}\n"
        f"📉 Low: ${dfi['low']:.6f}\n\n"
        f"💧 Volume: ${dfi['volume']:,.0f}\n"
        f"{warning}\n"
        f"🕒 {now} UTC\n\n"
        f"#DeFiChain #DFI #Crypto"
    )



    send_discord(discord_message)

    send_x(
    f"🚀 DeFiChain $DFI Daily Update\n\n"
    f"💰 ${dfi['usd']:.6f}\n"
    f"📊 24h: {emoji} {change:.2f}%\n\n"
    f"#DeFiChain #DFI"
)



except Exception as e:

    print("Fehler:")
    print(e)
