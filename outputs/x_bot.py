# ======================================
# DeFiChain Intelligence v5
# X Thread Bot (Optimiert)
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


def safe_change(value):
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "0.00"


def format_price(value):
    try:
        val = float(value)
        if val <= 0:
            return "N/A"
        if val < 0.01:
            return f"{val:.8f}"
        if val < 1:
            return f"{val:.6f}"
        if val < 100:
            return f"{val:.2f}"
        return f"{val:,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def format_large_number(value, suffix=""):
    """Formatierte Zahlen wie 412.50M oder 288.00K ausgeben."""
    if value is None or value == "":
        return "N/A"

    if isinstance(value, str):
        if value.strip().upper() == "N/A":
            return "N/A"
        cleaned = value.replace(",", "").replace("DFI", "").strip()
        try:
            val = float(cleaned)
        except ValueError:
            return value
    else:
        try:
            val = float(value)
        except (ValueError, TypeError):
            return "N/A"

    if val <= 0:
        return "N/A"

    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.2f}B{suffix}"
    if val >= 1_000_000:
        return f"{val / 1_000_000:.2f}M{suffix}"
    if val >= 1_000:
        return f"{val / 1_000:.1f}K{suffix}"

    return f"{val:,.2f}{suffix}"


def change_emoji(value):
    try:
        return "🟢" if float(value) >= 0 else "🔴"
    except (TypeError, ValueError):
        return "⚪"


def detect_language(insight):
    if isinstance(insight, str):
        match = re.search(r"\(([A-Z]{2})\)", insight)
        if match:
            return match.group(1).lower()
    return os.getenv("APP_LANG", "de")


def get_clients():
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        return None, None

    client_v2 = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    auth = tweepy.OAuth1UserHandler(
        api_key, api_secret, access_token, access_token_secret
    )
    api_v1 = tweepy.API(auth)

    return client_v2, api_v1


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
        client, api_v1 = get_clients()

        if client is None:
            print("⚠️ X (Twitter) API Keys fehlen.", flush=True)
            return False

        language = detect_language(insight)
        lang = load_language(language)

        if not isinstance(intelligence, dict):
            intelligence = {}
        if not isinstance(global_crypto, dict):
            global_crypto = {}
        if not isinstance(market, dict):
            market = {}
        if not isinstance(network, dict):
            network = {}
        if not isinstance(tokenomics, dict):
            tokenomics = {}

        # Markt-Daten extrahieren
        btc = global_crypto.get("bitcoin", {})
        eth = global_crypto.get("ethereum", {})
        dfi = market.get("dfi", {})

        btc_price = btc.get("price", "N/A")
        btc_change = safe_float(btc.get("change", 0))

        eth_price = eth.get("price", "N/A")
        eth_change = safe_float(eth.get("change", 0))

        dfi_price = dfi.get("price", "N/A")
        dfi_change = safe_float(dfi.get("change", 0))

        # Tokenomics auslesen
        burned_raw = tokenomics.get("burned_dfi", tokenomics.get("burned", 0))
        minted_raw = tokenomics.get("daily_minted", tokenomics.get("minted", 0))

        burned_dfi = format_large_number(burned_raw)
        daily_minted = format_large_number(minted_raw)

        score = intelligence.get("total", "N/A")
        status = intelligence.get("status", "N/A")
        daily_insight = intelligence.get("daily_insight", "")

        header_title = lang.get("header_title", "🚀 DeFiChain Daily Intelligence")
        intelligence_title = lang.get("intelligence", "🧠 Intelligence Score")
        network_title = lang.get("network", "Network")
        news_title = lang.get("news", "News")
        history_title = lang.get("history", "History")

        # ==================================
        # TWEET 1: PREISE & TOKENOMICS
        # ==================================
        post1 = f"""
{header_title} ({language.upper()})

🌍 BTC: ${format_price(btc_price)} ({change_emoji(btc_change)}{safe_change(btc_change)}%)
🌍 ETH: ${format_price(eth_price)} ({change_emoji(eth_change)}{safe_change(eth_change)}%)

💎 DFI: ${format_price(dfi_price)} ({change_emoji(dfi_change)}{safe_change(dfi_change)}%)
🔥 Burned: {burned_dfi} DFI
🪙 Daily Minted: {daily_minted} DFI

🧠 Score: {score}/100 ({status})

#DeFiChain #DFI
""".strip()

        if len(post1) > 280:
            post1 = post1[:277] + "..."

        result1 = client.create_tweet(text=post1)
        tweet1_id = result1.data["id"]

        # ==================================
        # TWEET 2: INSIGHTS & SCORE
        # ==================================
        post2 = f"""
🧠 {intelligence_title}

⭐ {score}/100 - {status}

💡 Daily Insight:

{daily_insight}
""".strip()

        if len(post2) > 280:
            post2 = post2[:277] + "..."

        result2 = client.create_tweet(
            text=post2,
            in_reply_to_tweet_id=tweet1_id
        )
        tweet2_id = result2.data["id"]

        # ==================================
        # TWEET 3: NETWORK & NEWS
        # ==================================
        network_status = network.get("network_status", "🟢 Online")

        post3 = f"""
⛓ {network_title}

{network_status}

📰 {news_title}
""".strip()

        if isinstance(insight, str):
            news_match = re.search(
                r"📰\s*News:\s*(.+?)(?:\n\n|📚|$)",
                insight,
                re.DOTALL
            )
            if news_match:
                extracted_news = news_match.group(1).strip()
                if extracted_news:
                    post3 += "\n\n" + extracted_news

        if len(post3) > 280:
            post3 = post3[:277] + "..."

        result3 = client.create_tweet(
            text=post3,
            in_reply_to_tweet_id=tweet2_id
        )
        tweet3_id = result3.data["id"]

        # ==================================
        # TWEET 4: HISTORY / CHAPTER
        # ==================================
        post4 = f"📚 {history_title}".strip()

        if current_history:
            history_id = current_history.get("id", "N/A")
            history_name = current_history.get("title", "DeFiChain Update")
            history_text = current_history.get("text", current_history.get("content", ""))

            post4 += f"\n\nChapter {history_id}\n{history_name}\n\n{history_text[:140]}"
        else:
            post4 += "\n\nDeFiChain ecosystem update."

        post4 += "\n\n#DeFiChain #DFI"

        if len(post4) > 280:
            post4 = post4[:277] + "..."

        client.create_tweet(
            text=post4,
            in_reply_to_tweet_id=tweet3_id
        )

        return True

    except Exception as e:
        print(f"❌ Fehler bei send_x_thread: {e}", flush=True)
        return False
