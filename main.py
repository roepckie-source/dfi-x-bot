import os
import requests
import tweepy
import json
from datetime import datetime


# ==============================
# ENVIRONMENT
# ==============================

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")


# ==============================
# ZAHLEN FORMATIEREN
# ==============================

def format_number(value):
    try:
        return f"{float(value):,.2f}"
    except:
        return "N/A"



# ==============================
# DFI MARKTDATEN
# ==============================

def get_dfi_data():

    result = {
        "usd": 0,
        "eur": 0,
        "change": 0,
        "high": 0,
        "low": 0,
        "volume": 0,
        "market_cap": 0,
        "circulating_supply": 0,
        "ath": 0,
        "ath_change": 0
    }


    try:

        url = "https://api.coingecko.com/api/v3/coins/defichain"

        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false"
        }


        response = requests.get(
            url,
            params=params,
            timeout=20
        )


        response.raise_for_status()

        data = response.json()

        market = data.get(
            "market_data",
            {}
        )


        result["usd"] = market.get(
            "current_price",
            {}
        ).get(
            "usd",
            0
        )


        result["eur"] = market.get(
            "current_price",
            {}
        ).get(
            "eur",
            0
        )


        result["change"] = market.get(
            "price_change_percentage_24h",
            0
        )


        result["high"] = market.get(
            "high_24h",
            {}
        ).get(
            "usd",
            0
        )


        result["low"] = market.get(
            "low_24h",
            {}
        ).get(
            "usd",
            0
        )


        result["volume"] = market.get(
            "total_volume",
            {}
        ).get(
            "usd",
            0
        )


        result["market_cap"] = market.get(
            "market_cap",
            {}
        ).get(
            "usd",
            0
        )


        result["circulating_supply"] = market.get(
            "circulating_supply",
            0
        )


        result["ath"] = market.get(
            "ath",
            {}
        ).get(
            "usd",
            0
        )


        result["ath_change"] = market.get(
            "ath_change_percentage",
            {}
        ).get(
            "usd",
            0
        )


    except Exception as e:

        print(
            "DFI Daten Fehler:",
            e
        )


    return result

# ==============================
# DUSD DATEN
# ==============================

def get_dusd_data():

    result = {
        "usd": 0,
        "eur": 0,
        "change": 0
    }


    try:

        url = "https://api.coingecko.com/api/v3/simple/price"


        params = {
            "ids": "decentralized-usd",
            "vs_currencies": "usd,eur",
            "include_24hr_change": "true"
        }


        response = requests.get(
            url,
            params=params,
            timeout=20
        )


        response.raise_for_status()

        data = response.json().get(
            "decentralized-usd",
            {}
        )


        result["usd"] = data.get(
            "usd",
            0
        )

        result["eur"] = data.get(
            "eur",
            0
        )

        result["change"] = data.get(
            "usd_24h_change",
            0
        )


    except Exception as e:

        print(
            "DUSD Fehler:",
            e
        )


    return result



# ==============================
# DEFICHAIN NETWORK
# ==============================

def get_network_data():

    result = {

        "existing_dfi": "N/A",
        "burned_dfi": "N/A",
        "locked_dusd": "N/A",
        "excess_dfi": "N/A"

    }


    try:

        url = (
            "https://ocean.defichain.com/"
            "v0/mainnet/stats"
        )


        response = requests.get(
            url,
            timeout=20
        )


        response.raise_for_status()


        data = response.json().get(
            "data",
            {}
        )


        result["existing_dfi"] = format_number(
            data.get(
                "circulatingSupply",
                0
            )
        )


        result["burned_dfi"] = format_number(
            data.get(
                "burned",
                0
            )
        )


        result["locked_dusd"] = format_number(
            data.get(
                "dusdLocked",
                0
            )
        )


        result["excess_dfi"] = format_number(
            data.get(
                "excessDFI",
                0
            )
        )


    except Exception as e:

        print(
            "Network Fehler:",
            e
        )


    return result



# ==============================
# NEWS LADEN
# ==============================

def get_dfi_news():

    try:

        with open(
            "dfi_news.json",
            "r",
            encoding="utf-8"
        ) as file:

            news = json.load(file)


        if not news:

            return {
                "title": "DeFiChain Daily",
                "text": "Keine News",
                "hashtags": "#DFI"
            }


        day = datetime.now().timetuple().tm_yday

        return news[
            (day - 1) % len(news)
        ]


    except Exception as e:

        print(
            "News Fehler:",
            e
        )


        return {

            "title": "DeFiChain Update",
            "text": "Daily Report",
            "hashtags": "#DeFiChain #DFI"

        }



# ==============================
# DISCORD
# ==============================

def send_discord(message):

    if not DISCORD_WEBHOOK:
        return


    try:

        response = requests.post(

            DISCORD_WEBHOOK,

            json={
                "content": message
            },

            timeout=20
        )


        if response.status_code == 204:

            print(
                "Discord Nachricht erfolgreich gesendet"
            )

        else:

            print(
                "Discord Fehler:",
                response.text
            )


    except Exception as e:

        print(
            "Discord Ausnahme:",
            e
        )



# ==============================
# X / TWITTER
# ==============================

def send_x(message):

    try:

        client = tweepy.Client(

            consumer_key=API_KEY,

            consumer_secret=API_SECRET,

            access_token=ACCESS_TOKEN,

            access_token_secret=ACCESS_TOKEN_SECRET

        )


        client.create_tweet(
            text=message[:280]
        )


        print(
            "X Tweet erfolgreich gesendet"
        )


    except Exception as e:

        print(
            "X Fehler:",
            e
        )



# ==============================
# HAUPTPROGRAMM
# ==============================

try:


    dfi = get_dfi_data()

    dusd = get_dusd_data()

    network = get_network_data()

    news = get_dfi_news()


    change = dfi["change"]


    emoji = (
        "🟢"
        if change >= 0
        else
        "🔴"
    )


    now = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )



    discord_message = f"""

🚀 **DeFiChain Daily Update**


💰 **DFI**

🇺🇸 ${dfi['usd']:.8f}

🇪🇺 €{dfi['eur']:.8f}


{emoji} **24h**

{change:.2f}%



📊 **Market**

High:
${dfi['high']:,.8f}

Low:
${dfi['low']:,.8f}

Volume:
${dfi['volume']:,.0f}

Market Cap:
${dfi['market_cap']:,.0f}

Circulating Supply:
{dfi['circulating_supply']:,.0f} DFI

🏆 ATH:
${dfi['ath']:.4f}

📉 From ATH:
{dfi['ath_change']:.2f}%



💵 **DUSD**

${dusd['usd']:.6f}

24h:
{dusd['change']:.2f}%



🌐 **Network**

Existing DFI:
{network['existing_dfi']}


🔥 Burned:
{network['burned_dfi']}


🔒 Locked dUSD:
{network['locked_dusd']}


⚖️ Excess DFI:
{network['excess_dfi']}



📰 **News**

{news['title']}

{news['text']}


{news['hashtags']}



🕒 {now}


https://defichain.com

"""


    x_message = f"""

🚀 DeFiChain $DFI Daily


💰 ${dfi['usd']:.8f}

🇪🇺 €{dfi['eur']:.8f}


{emoji} {change:.2f}%


📊 Market Cap:
${dfi['market_cap']:,.0f}


💵 DUSD:
${dusd['usd']:.6f}


📰 {news['title']}


#DeFiChain #DFI #DUSD

"""


    send_discord(
        discord_message
    )


    send_x(
        x_message
    )


except Exception as e:

    print(
        "Bot Fehler:",
        e
    )