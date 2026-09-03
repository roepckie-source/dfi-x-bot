# ======================================
# DeFiChain Intelligence v5
# X Thread Bot
# ======================================

import os
import re
import tweepy

from modules.language import load_language


# ======================================
# HELFER
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
            return f"{value / 1_000:.1f}K"

        return f"{value:.2f}"

    except (TypeError, ValueError):

        return "N/A"


def change_emoji(value):

    return (
        "🟢"
        if safe_float(value) >= 0
        else "🔴"
    )


def safe_truncate(
    text,
    max_chars=280
):

    if not isinstance(text, str):
        return ""

    text = text.strip()

    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars - 3]

    if " " in truncated:
        truncated = truncated.rsplit(
            " ",
            1
        )[0]

    return truncated + "..."


# ======================================
# X CLIENT
# ======================================

def get_twitter_client():

    try:

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

            print(
                "⚠️ X API Zugangsdaten fehlen."
            )

            return None

        return tweepy.Client(

            consumer_key=api_key,

            consumer_secret=api_secret,

            access_token=access_token,

            access_token_secret=access_token_secret

        )

    except Exception as e:

        print(
            "⚠️ Fehler beim Initialisieren "
            f"des X Clients: {e}"
        )

        return None


# ======================================
# SPRACHE
# ======================================

def detect_language(report):

    if isinstance(report, str):

        match = re.search(
            r"\(([A-Z]{2})\)",
            report
        )

        if match:

            return match.group(1).lower()

    return os.getenv(
        "APP_LANG",
        "de"
    )


# ======================================
# X THREAD
# ======================================

def send_x_thread(

    report="",

    tokenomics=None,

    dusd=None,

    network=None,

    intelligence=None,

    current_history=None,

    global_crypto=None,

    market=None

):

    try:

        # ==================================
        # CLIENT
        # ==================================

        client = get_twitter_client()

        if client is None:
            return False


        # ==================================
        # DATEN ABSICHERN
        # ==================================

        tokenomics = (
            tokenomics
            if isinstance(tokenomics, dict)
            else {}
        )

        dusd = (
            dusd
            if isinstance(dusd, dict)
            else {}
        )

        network = (
            network
            if isinstance(network, dict)
            else {}
        )

        intelligence = (
            intelligence
            if isinstance(intelligence, dict)
            else {}
        )

        global_crypto = (
            global_crypto
            if isinstance(global_crypto, dict)
            else {}
        )

        market = (
            market
            if isinstance(market, dict)
            else {}
        )


        # ==================================
        # SPRACHE
        # ==================================

        language = detect_language(
            report
        )

        lang = load_language(
            language
        )


        # ==================================
        # FLAGGEN
        # ==================================

        flags = (
            "🇩🇪 🇬🇧 🇺🇸 🇸🇻 🇺🇾 🇧🇷 🇦🇷 "
            "🇳🇴 🇸🇪 🇫🇮 🇿🇦 🇦🇺 🇳🇿 "
            "🇨🇳 🇯🇵 🇮🇳 🇮🇩 🇫🇷 🇪🇸 "
            "🇵🇹 🇷🇺 🇸🇦"
        )


        # ==================================
        # MARKT
        # ==================================

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
            "price",
            dfi.get(
                "usd",
                "N/A"
            )
        )

        dfi_change = safe_float(
            dfi.get(
                "change",
                0
            )
        )


        # ==================================
        # TOKENOMICS
        #
        # DIE KEYS ENTSPRECHEN JETZT
        # DIREKT tokenomics.py
        # ==================================

        burn = tokenomics.get(
            "burn",
            {}
        )

        if not isinstance(
            burn,
            dict
        ):

            burn = {}


        burn_address = burn.get(
            "address",
            0
        )

        burn_fees = burn.get(
            "fees",
            0
        )

        burn_auction = burn.get(
            "auction",
            0
        )

        burn_payback = burn.get(
            "payback",
            0
        )

        burn_total = burn.get(
            "total",
            0
        )

        emission = tokenomics.get(
            "emission",
            0
        )

        net_change = tokenomics.get(
            "net_change",
            0
        )

        tokenomics_status = tokenomics.get(
            "status",
            "N/A"
        )


        # ==================================
        # INTELLIGENCE
        # ==================================

        score = intelligence.get(
            "total",
            intelligence.get(
                "score",
                0
            )
        )

        status = intelligence.get(
            "status",
            "N/A"
        )

        daily_insight = intelligence.get(
            "daily_insight",
            intelligence.get(
                "insight",
                ""
            )
        )


        # ==================================
        # DUSD
        # ==================================

        dusd_price = dusd.get(
            "price",
            dusd.get(
                "usd",
                None
            )
        )

        peg_deviation = dusd.get(
            "peg_deviation",
            None
        )


        # ==================================
        # SPRACH-TEXTE
        # ==================================

        header_title = lang.get(
            "header_title",
            "🚀 DeFiChain Intelligence"
        )

        global_title = lang.get(
            "global_crypto",
            "Global Crypto"
        )

        intelligence_title = lang.get(
            "intelligence",
            "Intelligence Score"
        )

        tokenomics_title = lang.get(
            "tokenomics",
            "Tokenomics"
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


        # ==================================
        # TWEET 1
        # MARKET
        # ==================================

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

💎 DeFiChain DFI:
${format_price(dfi_price)}
{change_emoji(dfi_change)} {safe_change(dfi_change)}%

#DeFiChain #DFI
""".strip()


        post1 = safe_truncate(
            post1,
            280
        )


        print(
            "DEBUG-Tweet 1:"
        )

        print(post1)


        result1 = client.create_tweet(
            text=post1
        )

        tweet1_id = result1.data["id"]

        print(
            "✅ X Tweet 1 gesendet:",
            tweet1_id
        )


        # ==================================
        # TWEET 2
        # TOKENOMICS
        # ==================================

        net_sign = (
            "+"
            if safe_float(net_change) >= 0
            else ""
        )


        post2 = f"""
🔥 {tokenomics_title}

🔥 Total Burn: {format_large_number(burn_total)} DFI
🪙 Emission: {format_large_number(emission)} DFI
🔥 Net Change: {net_sign}{format_large_number(net_change)} DFI

📍 Address Burn: {format_large_number(burn_address)} DFI
💸 Fee Burn: {format_large_number(burn_fees)} DFI
🔨 Auction Burn: {format_large_number(burn_auction)} DFI
💰 Payback Burn: {format_large_number(burn_payback)} DFI

🧠 {intelligence_title}: {score}/100
{status}
""".strip()


        post2 = safe_truncate(
            post2,
            280
        )


        print(
            "DEBUG-Tweet 2:"
        )

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


        # ==================================
        # TWEET 3
        # DUSD + NETWORK + NEWS
        # ==================================

        network_status = network.get(
            "network_status",
            "🟢 Online"
        )


        dusd_lines = []

        if dusd_price is not None:

            dusd_lines.append(
                f"💵 dUSD: "
                f"${format_price(dusd_price)}"
            )

        if peg_deviation is not None:

            dusd_lines.append(
                f"📉 Peg: "
                f"{safe_float(peg_deviation):.2f}%"
            )


        # ==================================
        # NEWS
        # ==================================

        news_text = ""

        if isinstance(
            report,
            str
        ):

            match = re.search(

                r"📰\s*News:\s*(.+?)"
                r"(?:\n\n|📚|$)",

                report,

                re.DOTALL

            )

            if match:

                news_text = (
                    match.group(1)
                    .strip()
                )


        post3 = f"""
⛓ {network_title}

{network_status}

{" ".join(dusd_lines)}

📰 {news_title}

{news_text if news_text else "DeFiChain Daily Update"}

#DeFiChain #DFI
""".strip()


        post3 = safe_truncate(
            post3,
            280
        )


        print(
            "DEBUG-Tweet 3:"
        )

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


        # ==================================
        # TWEET 4
        # HISTORY
        # ==================================

        history_name = (
            "DeFiChain Update"
        )

        history_text = ""

        if isinstance(
            current_history,
            dict
        ):

            history_name = (
                current_history.get(
                    "title",
                    "DeFiChain Update"
                )
            )

            history_text = (
                current_history.get(
                    "text",
                    current_history.get(
                        "content",
                        ""
                    )
                )
            )


        post4 = f"""
📚 {history_title}

{history_name}

{history_text}

#DeFiChain #DFI
""".strip()


        post4 = safe_truncate(
            post4,
            280
        )


        print(
            "DEBUG-Tweet 4:"
        )

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
            "❌ X Fehler:"
        )

        print(e)

        return False
