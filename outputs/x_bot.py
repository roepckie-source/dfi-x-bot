# ======================================
# DeFiChain Intelligence v5
# X Thread Bot
# ======================================

import os
import tweepy


# ======================================
# X API Zugang
# ======================================

X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")


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


def safe_change(value):

    try:

        return f"{float(value):.2f}"

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

    comparison=None,

    news=None

):

    try:

        client = get_client()

        dfi = market.get(

            "dfi",

            {}

        )


        # ==================================
        # TWEET 1
        # Global Crypto + DeFiChain
        # ==================================

        btc = global_crypto.get(

            "bitcoin",

            {}

        ) if global_crypto else {}


        eth = global_crypto.get(

            "ethereum",

            {}

        ) if global_crypto else {}



        score = intelligence.get(

            "total",

            "N/A"

        )


        status = intelligence.get(

            "status",

            "N/A"

        )



        post1 = f"""
🚀 DeFiChain Daily Intelligence

🌍 Global Crypto

Bitcoin
💵 ${btc.get('price','N/A')}
📈 {safe_change(btc.get('change'))}%


Ethereum
💵 ${eth.get('price','N/A')}
📈 {safe_change(eth.get('change'))}%


💎 DeFiChain DFI

Price:
${dfi.get('usd','N/A')}

24h:
{safe_change(dfi.get('change'))}%


🧠 Intelligence Score

⭐ {score}/100
{status}


#DeFiChain #DFI
""".strip()
        
        print("DEBUG Tweet 1:")
        print(post1)

        
        result1 = client.create_tweet(

            text=post1

        )


        print(

            "X Tweet 1 gesendet:",

            result1.data["id"]

        )



        # ==================================
        # TWEET 2
        # DeFiChain Intelligence
        # ==================================


        net_burn = tokenomics.get(

            "balance",

            0

        )


        post2 = f"""
🔥 DeFiChain Tokenomics

🧠 Intelligence Score

⭐ {score}/100
{status}


🔥 Burn vs Emission

🟢 Burn exceeds emission

⚖️ Net Burn:

{short_number(net_burn)} DFI


⛓ Network

🟢 {network.get('network_status','N/A')}


💡 Daily Insight

{intelligence.get('daily_insight','DeFiChain analysis active')}


#DeFiChain #DFI
""".strip()

        if len(post2) > 280:

            post2 = post2[:277] + "..."



        result2 = client.create_tweet(

            text=post2,

            in_reply_to_tweet_id=result1.data["id"]

        )


        print(

            "X Tweet 2 gesendet:",

            result2.data["id"]

        )

        # ==================================
        # TWEET 3
        # DeFiChain Content Update
        # ==================================

        post3 = """
📰 DeFiChain Daily Update

""".strip()


        # ==============================
        # Content / History
        # ==============================

        if history:

            post3 += f"""

📚 Chapter {history.get(
    "id",
    "N/A"
)}

{history.get(
    "title",
    "DeFiChain Update"
)}

{history.get(
    "text",
    ""
)[:160]}
"""


        # ==============================
        # Fallback
        # ==============================

        else:

            post3 += """

DeFiChain ecosystem update active.

"""


        post3 += """

#DeFiChain #DFI
""".strip()



        # X Limit

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
