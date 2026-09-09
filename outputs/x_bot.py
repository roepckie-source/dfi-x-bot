# ======================================
# DeFiChain Intelligence v5
# X Thread Bot
# ======================================

import os
import re
import tweepy

from modules.language import load_language


def safe_float(value, default=0.0):

    try:
        return float(value)

    except (TypeError, ValueError):

        return default


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


def clean_text(text, max_len=160):

    if not text:
        return ""

    text = str(text).replace(
        "\n",
        " "
    ).strip()

    if len(text) <= max_len:
        return text

    shortened = text[:max_len - 3]

    if " " in shortened:
        shortened = shortened.rsplit(
            " ",
            1
        )[0]

    return shortened + "..."


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


def get_client():

    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

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


        # ======================================
        # NORMALISIEREN
        # ======================================

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


        # ======================================
        # LANGUAGE
        # ======================================

        language = detect_language(
            insight
        )

        lang = load_language(
            language
        )


        # ======================================
        # TRANSLATED LABELS
        # ======================================

        header_title = lang.get(
            "header_title",
            "🚀 DeFiChain Daily Intelligence"
        )

        global_title = lang.get(
            "global_crypto",
            "Global Crypto"
        )

        price_title = lang.get(
            "price",
            "Price"
        )

        change_title = lang.get(
            "change",
            "24h Change"
        )

        intelligence_title = lang.get(
            "intelligence",
            "Intelligence Score"
        )

        tokenomics_title = lang.get(
            "tokenomics",
            "Tokenomics"
        )

        burn_title = lang.get(
            "burn",
            "Burn"
        )

        emission_title = lang.get(
            "emission",
            "Emission"
        )

        network_title = lang.get(
            "network",
            "Network"
        )

        news_title = lang.get(
            "content_update",
            lang.get(
                "news",
                "Daily News"
            )
        )

        history_title = lang.get(
            "history",
            "DeFiChain History"
        )

        insight_title = lang.get(
            "insight",
            lang.get(
                "insight_title",
                "Daily Insight"
            )
        )


        # ======================================
        # MARKET DATA
        # ======================================

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


        # ======================================
        # TOKENOMICS
        # ======================================

        burn = tokenomics.get(
            "burn",
            {}
        )

        total_burn = burn.get(
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

        address_burn = burn.get(
            "address",
            0
        )

        fees_burn = burn.get(
            "fees",
            0
        )

        auction_burn = burn.get(
            "auction",
            0
        )

        payback_burn = burn.get(
            "payback",
            0
        )


        # ======================================
        # INTELLIGENCE
        # ======================================

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


        # ======================================
        # dUSD
        # ======================================

        dusd_price = dusd.get(
            "price",
            "N/A"
        )

        dusd_health = dusd.get(
            "health_score",
            "N/A"
        )


        # ======================================
        # NETWORK
        # ======================================

        network_status = network.get(
            "network_status",
            "🟢 Online"
        )


        # ======================================
        # FLAGS
        # ======================================

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
{change_emoji(btc_change)} {btc_change:.2f}%

Ξ Ethereum:
${format_price(eth_price)}
{change_emoji(eth_change)} {eth_change:.2f}%

💎 DeFiChain DFI

{price_title}:
${format_price(dfi_price)}

{change_title}:
{change_emoji(dfi_change)} {dfi_change:.2f}%

#DeFiChain #DFI
""".strip()

        if len(post1) > 280:
            post1 = post1[:277] + "..."


        # ==================================================
        # TWEET 2
        # ==================================================

        post2 = f"""
🔥 {tokenomics_title}

{burn_title}:
{format_large_number(total_burn)} DFI

{emission_title}:
{format_large_number(emission)} DFI

Net Change:
{format_large_number(net_change)} DFI

• Address: {format_large_number(address_burn)}
• Fees: {format_large_number(fees_burn)}
• Auction: {format_large_number(auction_burn)}
• Payback: {format_large_number(payback_burn)}

🧠 {intelligence_title}:
{score}/100

{status}

💡 {insight_title}:
{clean_text(daily_insight, 80)}
""".strip()

        if len(post2) > 280:
            post2 = post2[:277] + "..."


        # ==================================================
        # TWEET 3
        # ==================================================

        news_text = ""

        if isinstance(
            insight,
            str
        ):

            news_match = re.search(
                r"📰\s*(?:News|Noticias|Nachrichten|Новости|समाचार|Berita):\s*(.+?)(?:\n\n|📚|$)",
                insight,
                re.DOTALL
            )

            if news_match:

                news_text = news_match.group(1).strip()


        if not news_text:

            news_text = clean_text(
                insight,
                100
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
            post3 = post3[:277] + "..."


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
                f"{clean_text(history_text, 120)}"
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
            post4 = post4[:277] + "..."


        # ==================================================
        # SEND THREAD
        # ==================================================

        print("DEBUG Tweet 1:")
        print(post1)

        res1 = client.create_tweet(
            text=post1
        )

        tweet1_id = res1.data["id"]

        logging_message = (
            f"✅ Tweet 1 ({language.upper()}) gesendet: "
            f"{tweet1_id}"
        )

        print(logging_message)


        print("DEBUG Tweet 2:")
        print(post2)

        res2 = client.create_tweet(
            text=post2,
            in_reply_to_tweet_id=tweet1_id
        )

        tweet2_id = res2.data["id"]

        print(
            f"✅ Tweet 2 ({language.upper()}) gesendet: "
            f"{tweet2_id}"
        )


        print("DEBUG Tweet 3:")
        print(post3)

        res3 = client.create_tweet(
            text=post3,
            in_reply_to_tweet_id=tweet2_id
        )

        tweet3_id = res3.data["id"]

        print(
            f"✅ Tweet 3 ({language.upper()}) gesendet: "
            f"{tweet3_id}"
        )


        print("DEBUG Tweet 4:")
        print(post4)

        res4 = client.create_tweet(
            text=post4,
            in_reply_to_tweet_id=tweet3_id
        )

        print(
            f"✅ Tweet 4 ({language.upper()}) gesendet: "
            f"{res4.data['id']}"
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
