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
# X THREAD
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


💰 Price

${dfi.get('usd',0):.8f}

🇪🇺 €{dfi.get('eur',0):.8f}


{format_percent(
    dfi.get('usd_24h_change',0)
)}


📊 Market Cap

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

{comparison['vs_eth']}""",



f"""🌐 DeFiChain Network


🔥 Burned DFI:

{network['burned_dfi']}


🔒 Locked dUSD:

{network['locked_dusd']}


📰 Daily Insight

{news['title']}

{news['text']}


{news['hashtags']}

#DeFiChain #DFI"""
        ]


             for tweet in tweets:

            # X Limit Sicherheit
            tweet = tweet[:280]


            response = client.create_tweet(
                text=tweet
            )


            print(
                "X Tweet gesendet:",
                response.data["id"]
            )


        print(
            "X Thread erfolgreich gesendet"
        )


    except Exception as e:

        print(
            "X Thread Fehler:",
            e
        )
