import tweepy

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
# X TEST POST
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


        tweet = f"""
🚀 DeFiChain $DFI Daily Update 🌍


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


#DeFiChain #DFI
"""


        response = client.create_tweet(
            text=tweet
        )


        print(
            "X Tweet erfolgreich gesendet:",
            response.data["id"]
        )


    except Exception as e:

        print(
            "X Fehler:",
            e
        )
