# ======================================
# DeFiChain Intelligence v5
# X Thread Bot
# ======================================

import os
import re
import tweepy

from modules.language import load_language


# ======================================
# FORMAT HELPERS
# ======================================

def safe_float(value, default=0.0):

    try:
        return float(value)

    except (TypeError, ValueError):

        return default


def safe_change(value):

    try:
        return f"{float(value):.2f}"

    except (TypeError, ValueError):

        return "0.00"


def format_price(value):

    try:

        value = float(value)

        if value < 0.01:
            return f"{value:.8f}"

        if value < 1:
            return f"{value:.6f}"

        if value < 100:
            return f"{value:.2f}"

        return f"{value:,.2f}"

    except (TypeError, ValueError):

        return "N/A"


def format_large_number(value):

    try:

        value = float(value)

        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"

        if value >= 1_000:
            return f"{value / 1_000:.2f}K"

        return f"{value:,.2f}"

    except (TypeError, ValueError):

        return "N/A"


def change_emoji(value):

    try:

        return (
            "🟢"
            if float(value) >= 0
            else "🔴"
        )

    except (TypeError, ValueError):

        return "⚪"


def clean_text(text, max_len=180):

    if not text:
        return ""

    text = str(text).replace(
        "\n",
        " "
    ).strip()

    if len(text) <= max_len:
        return text

    shortened = text[
        :max_len - 3
    ]

    if " " in shortened:
        shortened = shortened.rsplit(
            " ",
            1
        )[0]

    return shortened + "..."


# ======================================
# LANGUAGE
# ======================================

def detect_language(insight):

    if isinstance(insight, str):

        match = re.search(
            r"\(([A-Z]{2})\)",
            insight
        )

        if match:
            return match.group(1).lower()

    return os.getenv(
        "APP_LANG",
        "de"
    )


# ======================================
# X CLIENT
# ======================================

def get_client():

    api_key = os.getenv(
        "X_API_KEY"
    )

    api_secret = os.getenv(
        "X_API_SECRET"
    )

    access_token = os.getenv(
        "X_ACCESS_TOKEN"
    )

    access_token_secret = os.getenv(
        "X_ACCESS_TOKEN_SECRET"
    )

    if not all([
        api_key,
        api_secret,
        access_token,
        access_token_secret
    ]):

        return None

    return tweepy.Client(

        consumer_key=api_key,
        consumer_secret=api_secret,

        access_token=access_token,
        access_token_secret=access_token_secret
    )


# ======================================
# SEND X THREAD
# ======================================

def send_x_thread(

    insight,

    tokenomics=None,

    dusd=None,

    network=None,

    intelligence=None,

    current_history=None,

    global_crypto=None,

    market=None

):

    try:

        client = get_client()

        if client is None:

            print(
                "⚠️ X API Credentials fehlen."
            )

            return False


        # ----------------------------------
        # NORMALISIEREN
        # ----------------------------------

        if not isinstance(
            tokenomics,
            dict
        ):
            tokenomics = {}

        if not isinstance(
            dusd,
            dict
        ):
            dusd = {}

        if not isinstance(
            network,
            dict
        ):
            network = {}

        if not isinstance(
            intelligence,
            dict
        ):
            intelligence = {}

        if not isinstance(
            global_crypto,
            dict
        ):
            global_crypto = {}

        if not isinstance(
            market,
            dict
        ):
            market = {}


        # ----------------------------------
        # LANGUAGE
        # ----------------------------------

        language = detect_language(
            insight
        )

        lang = load_language(
            language
        )


        # ----------------------------------
        # MARKET
        # ----------------------------------

        btc = global_crypto.get(
            "bitcoin",
            {}
        )

        eth = global_crypto.get(
            "ethereum",
            {}
        )

        dfi = market.get(
            "dfi",
            {}
        )


        btc_price = btc.get(
            "price",
            "N/A"
        )

        btc_change = safe_float(
            btc.get(
                "change",
                0
            )
        )


        eth_price = eth.get(
            "price",
            "N/A"
        )

        eth_change = safe_float(
            eth.get(
                "change",
                0
            )
        )


        dfi_price = dfi.get(
            "usd",
            dfi.get(
                "price",
                "N/A"
            )
        )

        dfi_change = safe_float(
            dfi.get(
                "change",
                0
            )
        )


        # ----------------------------------
        # TOKENOMICS
        # ----------------------------------

        burn = tokenomics.get(
            "burn",
            {}
        )

        total_burn = safe_float(
            burn.get(
                "total",
                0
            )
        )

        emission = safe_float(
            tokenomics.get(
                "emission",
                0
            )
        )

        net_change = safe_float(
            tokenomics.get(
                "net_change",
                0
            )
        )


        address_burn = safe_float(
            burn.get(
                "address",
                0
            )
        )

        fees_burn = safe_float(
            burn.get(
                "fees",
                0
            )
        )

        auction_burn = safe_float(
            burn.get(
                "auction",
                0
            )
        )

        payback_burn = safe_float(
            burn.get(
                "payback",
                0
            )
        )


        # ----------------------------------
        # INTELLIGENCE
        # ----------------------------------

        score = intelligence.get(
            "total",
            "N/A"
        )

        status = intelligence.get(
            "status",
            "N/A"
        )

        daily_insight = intelligence.get(
            "daily_insight",
            ""
        )


        # ----------------------------------
        # dUSD
        # ----------------------------------

        dusd_price = dusd.get(
            "price",
            "N/A"
        )

        dusd_health = dusd.get(
            "health_score",
            "N/A"
        )


        # ----------------------------------
        # NETWORK
        # ----------------------------------

        network_status = network.get(
            "network_status",
            "🟢 Online"
        )


        # ----------------------------------
        # LANGUAGE LABELS
        # ----------------------------------

        header_title = lang.get(
            "header_title",
            "🚀 DeFiChain Daily Intelligence"
        )

        global_title = lang.get(
            "global_crypto",
            "Global Crypto"
        )

        intelligence_title = lang.get(
            "intelligence",
            "Intelligence Score"
        )

        market_title = lang.get(
            "market",
            "Market"
        )

        price_title = lang.get(
            "price",
            "Price"
        )

        change_title = lang.get(
            "change_24h",
            "24h"
        )

        network_title = lang.get(
            "network",
            "Network"
        )

        news_title = lang.get(
            "news",
            "News"
        )

        history_title = lang.get(
            "history",
            "History"
        )


        # ----------------------------------
        # FLAGS
        # ----------------------------------

        flags = (
            "🇩🇪 🇬🇧 🇺🇸 🇸🇻 🇺🇾 🇧🇷 🇦🇷 "
            "🇳🇴 🇸🇪 🇫🇮 🇿🇦 🇦🇺 🇳🇿 "
            "🇨🇳 🇯🇵 🇮🇳 🇮🇩 🇫🇷 🇪🇸 "
            "🇵🇹 🇷🇺 🇸🇦"
        )


        # ==================================================
        # TWEET 1
        # ==================================================

        post1 = f"""
{header_title} ({language.upper()})

🌍 {flags}

🌍 {global_title}

₿ Bitcoin:
${format_price(btc_price)}
{change_emoji(btc_change)} {safe_change(btc_change)}%

Ξ Ethereum:
${format_price(eth_price)}
{change_emoji(eth_change)} {safe_change(eth_change)}%

💎 DeFiChain DFI

{price_title}:
${format_price(dfi_price)}

{change_title}:
{change_emoji(dfi_change)} {safe_change(dfi_change)}%

#DeFiChain #DFI
""".strip()


        if len(post1) > 280:

            post1 = (
                post1[:277]
                + "..."
            )


        print("DEBUG Tweet 1:")
        print(post1)


        result1 = client.create_tweet(
            text=post1
        )

        tweet1_id = result1.data["id"]

        print(
            "✅ X Tweet 1 gesendet:",
            tweet1_id
        )


        # ==================================================
        # TWEET 2
        # ==================================================

        post2 = f"""
🔥 Tokenomics

Burn:
{format_large_number(total_burn)} DFI

Emission:
{format_large_number(emission)} DFI

Net Change:
{format_large_number(net_change)} DFI

• Address Burn: {format_large_number(address_burn)}
• Fees Burn: {format_large_number(fees_burn)}
• Auction Burn: {format_large_number(auction_burn)}
• Payback Burn: {format_large_number(payback_burn)}

🧠 {intelligence_title}:
{score}/100

{status}

💡 {clean_text(daily_insight, 100)}
""".strip()


        if len(post2) > 280:

            post2 = (
                post2[:277]
                + "..."
            )


        print("DEBUG Tweet 2:")
        print(post2)


        result2 = client.create_tweet(

            text=post2,

            in_reply_to_tweet_id=tweet1_id
        )

        tweet2_id = result2.data["id"]


        print(
            "✅ X Tweet 2 gesendet:",
            tweet2_id
        )


        # ==================================================
        # TWEET 3
        # ==================================================

        news_text = ""

        if isinstance(
            insight,
            str
        ):

            news_match = re.search(

                r"📰\s*News:\s*(.+?)(?:\n\n|📚|$)",

                insight,

                re.DOTALL
            )

            if news_match:

                news_text = (
                    news_match.group(1)
                    .strip()
                )


        if not news_text:

            if isinstance(
                insight,
                str
            ):

                news_text = clean_text(
                    insight,
                    150
                )


        post3 = f"""
⛓ {network_title}

{network_status}

💵 dUSD:
${format_price(dusd_price)}

🩺 dUSD Health:
{dusd_health}

📰 {news_title}:
{news_text}
""".strip()


        if len(post3) > 280:

            post3 = (
                post3[:277]
                + "..."
            )


        print("DEBUG Tweet 3:")
        print(post3)


        result3 = client.create_tweet(

            text=post3,

            in_reply_to_tweet_id=tweet2_id
        )

        tweet3_id = result3.data["id"]


        print(
            "✅ X Tweet 3 gesendet:",
            tweet3_id
        )


        # ==================================================
        # TWEET 4
        # ==================================================

        post4 = f"""
📚 {history_title}
""".strip()


        if current_history:

            history_id = current_history.get(
                "id",
                "N/A"
            )

            history_name = current_history.get(
                "title",
                "DeFiChain Update"
            )

            history_text = current_history.get(
                "text",
                current_history.get(
                    "content",
                    ""
                )
            )

            post4 += (

                f"\n\n"
                f"Chapter {history_id}\n"
                f"{history_name}\n\n"
                f"{clean_text(history_text, 130)}"

            )

        else:

            post4 += (
                "\n\n"
                "DeFiChain ecosystem update."
            )


        post4 += (
            "\n\n"
            "#DeFiChain #DFI"
        )


        if len(post4) > 280:

            post4 = (
                post4[:277]
                + "..."
            )


        print("DEBUG Tweet 4:")
        print(post4)


        result4 = client.create_tweet(

            text=post4,

            in_reply_to_tweet_id=tweet3_id
        )


        print(
            "✅ X Tweet 4 gesendet:",
            result4.data["id"]
        )

        print(
            "🎉 X Thread erfolgreich gesendet!"
        )

        return True


    except Exception as e:

        print(
            "❌ Fehler beim Senden an X:"
        )

        print(
            e
        )

        return False
