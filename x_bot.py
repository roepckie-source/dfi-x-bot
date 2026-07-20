import tweepy
from datetime import datetime

from config import (
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

from utils import (
    format_percent,
    format_large_number
)


# ==============================
# X TEXT SICHERHEIT
# ==============================


def clean_x_text(text, max_length=180):

    if not text:
        return ""

    text = str(text)

    text = (
        text
        .replace("\n\n\n", "\n\n")
        .strip()
    )

    return text[:max_length]



# ==============================
# X POSTS
# ==============================


def send_x_thread(
    market,
    network,
    comparison,
    news
):

    try:

        client = tweepy.Client(

            consumer_key=API_KEY,

            consumer_secret=API_SECRET,

            access_token=ACCESS_TOKEN,

            access_token_secret=ACCESS_TOKEN_SECRET

        )


        dfi = market["dfi"]

        btc = market["bitcoin"]

        eth = market["ethereum"]



        tweets = [



f"""🚀 DeFiChain $DFI Daily Update 🌍


🇬🇧 English:
DeFiChain Daily Update


🇨🇳 中文:
DeFiChain 每日更新


🇮🇳 हिन्दी:
DeFiChain दैनिक अपडेट


🇸🇦 العربية:
تحديث DeFiChain اليومي


🇮🇩 Indonesia:
Update Harian DeFiChain


🇪🇸 Español:
Actualización diaria de DeFiChain


🇫🇷 Français:
Mise à jour quotidienne DeFiChain


💰 Price:

${dfi.get('usd',0):.8f}

🇪🇺 €{dfi.get('eur',0):.8f}


{format_percent(
    dfi.get('usd_24h_change',0)
)}


📊 Market Cap:

${format_large_number(
    dfi.get('usd_market_cap',0)
)}


#DeFiChain #DFI""",




f"""🌍 Crypto Market Comparison


₿ Bitcoin

{format_percent(
    btc.get('usd_24h_change',0)
)}


Ξ Ethereum

{format_percent(
    eth.get('usd_24h_change',0)
)}


🚀 DFI

{format_percent(
    dfi.get('usd_24h_change',0)
)}


{comparison['vs_btc']}

{comparison['vs_eth']}


#Crypto""",




f"""📰 DeFiChain Daily Insight


{clean_x_text(
    news.get('title','DeFiChain Update')
)}


{clean_x_text(
    news.get('text','Daily DeFiChain Report')
)}


#DeFiChain #DFI"""
        ]



        # ==============================
        # POSTS SENDEN
        # ==============================


        for tweet in tweets:


            tweet = tweet[:280]


            response = client.create_tweet(

                text=tweet

            )


            print(

                "X Tweet gesendet:",

                response.data["id"]

            )



        print(

            "X Posts erfolgreich gesendet"

        )



    except Exception as e:


        print(

            "X Fehler:",

            e

        )
