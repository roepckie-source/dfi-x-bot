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
# X THREAD POSTS
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


        hashtags = news.get(
            "hashtags",
            "#DeFiChain #DFI"
        )


        tweets = [

f"""🚀 DeFiChain $DFI Daily Update 🌍


📅 {news.get('date','')}


🤖 Daily Report #{news.get('report','')}


🌐 Global Crypto Update:

🇬🇧 🇨🇳 🇮🇳 🇸🇦 🇮🇩 🇪🇸 🇫🇷


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


📅 {news.get('date','')}


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


{comparison.get('vs_btc','')}

{comparison.get('vs_eth','')}


#Crypto""",



f"""📰 DeFiChain Daily Insight


📅 {news.get('date','')}


🤖 Report #{news.get('report','')}


📚 History #{news.get('id',0)}/100


🎯 {news.get('title','')}


{news.get('text','')}


{hashtags}"""

        ]


        previous_tweet_id = None


        for index, tweet in enumerate(
            tweets,
            start=1
        ):

            print("----------------")
            print(
                f"Sende Tweet Nummer: {index}"
            )


            # X Zeichenlimit
            tweet = tweet[:280]


            if previous_tweet_id:


                response = client.create_tweet(

                    text=tweet,

                    in_reply_to_tweet_id=previous_tweet_id

                )


            else:


                response = client.create_tweet(

                    text=tweet

                )


            previous_tweet_id = response.data["id"]


            print(
                "X Tweet gesendet:",
                previous_tweet_id
            )


        print(
            "X Posts erfolgreich gesendet"
        )


    except Exception as e:

        print(
            "X Fehler:",
            e
        )
