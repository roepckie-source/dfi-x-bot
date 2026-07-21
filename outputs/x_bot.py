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
# X EINZELPOST
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


        tweet = f"""🚀 DeFiChain $DFI Daily Update 🌍


📅 {news.get('date','')}

🤖 Report #{news.get('report','')}

📚 History #{news.get('id',0)}/100


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


🎯 {news.get('title','')}


{news.get('text','')}


#DeFiChain #DFI
"""


        # X Limit Sicherheit

        tweet = tweet[:280]


        print("----------------")
        print("Sende X Daily Update")


        response = client.create_tweet(
            text=tweet
        )


        print(
            "X Tweet gesendet:",
            response.data["id"]
        )


        print(
            "X Post erfolgreich"
        )


    except Exception as e:


        error_message = str(e)


        if "403" in error_message:

            print(
                "⚠️ X Posting aktuell nicht möglich"
            )

            print(
                error_message
            )

            print(
                "Discord läuft weiter"
            )


        else:

            print(
                "⚠️ X Fehler:",
                error_message
            )

