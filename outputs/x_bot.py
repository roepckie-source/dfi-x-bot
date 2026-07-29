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
        # POST 1 MARKET
        # ==============================


        post1 = f"""
🚀 DeFiChain Market Update

💎 DFI
${dfi.get('usd','N/A')}

📊 24h
{dfi.get('change','N/A')}%

🏦 Market Cap
${short_number(dfi.get('market_cap'))}

#DeFiChain #DFI
""".strip()



        result1 = client.create_tweet(

            text=post1

        )


        print(

            "X Tweet 1 gesendet:",

            result1.data["id"]

        )





        # ==============================
        # POST 2 TOKENOMICS
        # ==============================


        burn = tokenomics.get(

            "burn",

            {}

        )


        post2 = f"""
🔥 DeFiChain Tokenomics

🔥 Burn > Emission

⚖️ Net balance:

{short_number(
    tokenomics.get("balance")
)} DFI


⛓ Network:

{network.get(
    "network_status",
    "N/A"
)}

The fundamentals remain strong.

#DeFiChain #DFI
""".strip()



        result2 = client.create_tweet(

            text=post2,

            in_reply_to_tweet_id=result1.data["id"]

        )


        print(

            "X Tweet 2 gesendet:",

            result2.data["id"]

        )





        # ==============================
        # POST 3 INTELLIGENCE + HISTORY
        # ==============================


        score = intelligence.get(

            "total",

            "N/A"

        )


        status = intelligence.get(

            "status",

            "N/A"

        )



        post3 = f"""
🧠 DeFiChain Intelligence

⭐ Daily Score

{score}/100

{status}


🔥 Tokenomics:
Strong


⚠️ Main Risk:
dUSD stability


Tracking:

Market | Health | Network
""".strip()





        # ==============================
        # HISTORY INSIGHT
        # ==============================


        if history:


            post3 += f"""

📚 History

{history.get(
    "title",
    "DeFiChain"
)}

💡 {history.get(
    "text",
    ""
)[:60]}...
"""
       
    
        post3 += """

#DeFiChain #DFI
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
