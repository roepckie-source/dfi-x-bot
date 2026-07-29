# ======================================
# DeFiChain Intelligence v5
# X / Twitter Thread Bot
# ======================================


import os
import tweepy



# ======================================
# X API Zugang
# ======================================


X_API_KEY = os.environ.get(
    "X_API_KEY"
)

X_API_SECRET = os.environ.get(
    "X_API_SECRET"
)

X_ACCESS_TOKEN = os.environ.get(
    "X_ACCESS_TOKEN"
)

X_ACCESS_SECRET = os.environ.get(
    "X_ACCESS_SECRET"
)




# ======================================
# X Client
# ======================================


def get_client():

    return tweepy.Client(

        consumer_key=X_API_KEY,

        consumer_secret=X_API_SECRET,

        access_token=X_ACCESS_TOKEN,

        access_token_secret=X_ACCESS_SECRET

    )





# ======================================
# Format Helfer
# ======================================


def short_number(value):

    try:

        value = float(value)


        if value >= 1_000_000:

            return f"{value/1_000_000:.2f}M"


        if value >= 1_000:

            return f"{value/1_000:.2f}K"


        return f"{value:.2f}"


    except:

        return "N/A"





# ======================================
# X Thread senden
# ======================================


def send_x_thread(

    market,

    tokenomics,

    dusd,

    network,

    intelligence,

    history=None,

    global_crypto=None,

    comparison=None

):

    try:


        client = get_client()



        dfi = market.get(

            "dfi",

            {}

        )



        # ==============================
        # POST 1 GLOBAL CRYPTO
        # ==============================


        post1 = f"""
🌍 Global Crypto Update

₿ Bitcoin

💵 Price
${global_crypto.get("bitcoin", {}).get("price", "N/A")}

📈 24h
{global_crypto.get("bitcoin", {}).get("change", 0):.2f} %

━━━━━━━━━━

Ξ Ethereum

💵 Price
${global_crypto.get("ethereum", {}).get("price", "N/A")}

📈 24h
{global_crypto.get("ethereum", {}).get("change", 0):.2f} %

#Bitcoin #Ethereum #Crypto
""".strip()


        result1 = client.create_tweet(

            text=post1

        )


        print(

            "X Tweet 1 gesendet:",

            result1.data["id"]

        )





        # ==============================
        # POST 2 DEFICHAIN MARKET UPDATE
        # ==============================


        score = intelligence.get(
            "total",
            "N/A"
        )


        post2 = f"""
🚀 DeFiChain Daily Market Update

💎 DFI

💵 Price
${dfi.get('usd','N/A')}

📈 24h
{dfi.get('change','N/A')} %

🏦 Market Cap
${short_number(dfi.get('market_cap'))}


🧠 Intelligence Score

⭐ {score}/100


🔥 Tokenomics

🟢 Burn exceeds emission


        result2 = client.create_tweet(

            text=post2,

            in_reply_to_tweet_id=result1.data["id"]

        )

        print(

            "X Tweet 2 gesendet:",

            result2.data["id"]

        )



        # ==============================
        # POST 3 CRYPTO MARKET COMPARISON
        # ==============================


        post3 = f"""
📊 Crypto Market Comparison

₿ Bitcoin

📈 24h
{comparison.get("bitcoin", "N/A"):.2f} %


Ξ Ethereum

📈 24h
{comparison.get("ethereum", "N/A"):.2f} %


🔹 DeFiChain DFI

📈 24h
{comparison.get("dfi", "N/A"):.2f} %


💡 Daily Insight

{status if 'status' in locals() else "DeFiChain Intelligence"}

#Bitcoin #Ethereum #DeFiChain #DFI
""".strip()



        # X Zeichenlimit absichern

        if len(post3) > 280:

            post3 = post3[:277] + "..."

        result3 = client.create_tweet(

            text=post3,

            in_reply_to_tweet_id=result2.data["id"]

        )


        print(

            "X Tweet 3 gesendet:",

            result3.data["id"]

        )



        print(

            "X Thread erfolgreich"

        )




    except Exception as e:


        print(

            "⚠️ X Posting aktuell nicht möglich"

        )


        print(e)
