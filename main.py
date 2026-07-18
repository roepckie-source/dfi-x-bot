import os
import requests
import tweepy
import json
from datetime import datetime


# ==============================
# ENVIRONMENT
# ==============================

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]



# ==============================
# ZAHLEN FORMATIEREN
# ==============================

def format_number(value):

    try:
        return f"{float(value):,.3f}"

    except:
        return "N/A"



# ==============================
# DFI MARKTDATEN
# ==============================

def get_dfi_data():

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
print(data)


    market = data["market_data"]


    return {

        "usd":
            market["current_price"]["usd"],

        "eur":
            market["current_price"]["eur"],

        "change":
            market["price_change_percentage_24h"],

        "high":
            market["high_24h"]["usd"],

        "low":
            market["low_24h"]["usd"],

        "volume":
            market["total_volume"]["usd"]

    }



# ==============================
# DUSD DATEN
# ==============================

def get_dusd_data():

    url = "https://api.coingecko.com/api/v3/simple/price"


    params = {

        "ids":
        "decentralized-usd",

        "vs_currencies":
        "usd,eur",

        "include_24hr_change":
        "true"

    }


    response = requests.get(

        url,
        params=params,
        timeout=20

    )


    response.raise_for_status()


    data = response.json()["decentralized-usd"]


    return {

        "usd":
            data["usd"],

        "eur":
            data["eur"],

        "change":
            data["usd_24h_change"]

    }

# ==============================
# DEFICHAIN NETWORK DATEN
# ==============================

def get_network_data():

    result = {

        "existing_dfi": "N/A",
        "burned_dfi": "N/A",
        "locked_dusd": "N/A",
        "excess_dfi": "N/A",
        "community_dfi": "N/A",
        "community_dusd": "N/A"

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


        data = response.json()


        stats = data.get(
            "data",
            {}
        )


        if "circulatingSupply" in stats:

            result["existing_dfi"] = format_number(
                stats["circulatingSupply"]
            )


        if "burned" in stats:

            result["burned_dfi"] = format_number(
                stats["burned"]
            )


        if "dusdLocked" in stats:

            result["locked_dusd"] = format_number(
                stats["dusdLocked"]
            )


        if "excessDFI" in stats:

            result["excess_dfi"] = format_number(
                stats["excessDFI"]
            )


        return result



    except Exception as e:

        print(
            "Network Daten Fehler:",
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


        day = datetime.now().timetuple().tm_yday


        index = (
            day - 1
        ) % len(news)


        return news[index]



    except Exception as e:

        print(
            "News Fehler:",
            e
        )


        return {

            "title":
            "Keine News verfügbar",

            "text":
            "DeFiChain Daily Update",

            "hashtags":
            "#DeFiChain"

        }





# ==============================
# DISCORD SENDEN
# ==============================

def send_discord(message):

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
                response.text
            )


    except Exception as e:

        print(
            "Discord Fehler:",
            e
        )





# ==============================
# X SENDEN
# ==============================

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


        print(
            "X Tweet erfolgreich gesendet"
        )


        print(response)



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



    # ==============================
    # DISCORD REPORT
    # ==============================

    discord_message = f"""

🚀 **DeFiChain Daily Report**


💰 **DFI Preis**

🇺🇸 USD:
${dfi['usd']:.8f}

🇪🇺 EUR:
€{dfi['eur']:.8f}


{emoji} **24h Änderung**

{change:.2f}%



💵 **DUSD**

🇺🇸 USD:
${dusd['usd']:.6f}

🇪🇺 EUR:
€{dusd['eur']:.6f}

📊 24h:
{dusd['change']:.2f}%



📈 **Market Daten**

High:
${dfi['high']:,.8f}

Low:
${dfi['low']:,.8f}

Volumen:
${dfi['volume']:,.0f}



📊 **DeFiChain Netzwerk**

🟢 Existing DFI:

{network['existing_dfi']}


🔥 Burned DFI:

{network['burned_dfi']}


🔒 Locked dUSD:

{network['locked_dusd']}


⚖️ Excess DFI:

{network['excess_dfi']}



🏦 **Community Fund**

💰 DFI:

{network['community_dfi']}


💵 dUSD:

{network['community_dusd']}



📰 **Daily News**

{news['title']}

{news['text']}


{news['hashtags']}



🕒 {now}


🔗 https://defichain.com

"""


    # ==============================
    # X POST
    # ==============================

    x_message = f"""

🚀 DeFiChain $DFI Daily Update


💰 DFI

🇺🇸 ${dfi['usd']:.8f}

🇪🇺 €{dfi['eur']:.8f}


📊 24h:

{emoji} {change:.2f}%


💵 DUSD

${dusd['usd']:.6f}



📊 Network

🟢 Existing DFI:
{network['existing_dfi']}

🔥 Burned:
{network['burned_dfi']}

🔒 Locked dUSD:
{network['locked_dusd']}



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
        "Fehler im Bot:"
    )

    print(e)
