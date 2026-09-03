# ======================================
# DeFiChain Intelligence v5
# X Thread Bot (inkl. GIF Support)
# ======================================

import os
import re
import tweepy

from modules.language import load_language


# ======================================
# FORMAT HELFER
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


def change_emoji(value):
    try:
        return "🟢" if float(value) >= 0 else "🔴"
    except (TypeError, ValueError):
        return "⚪"


# ======================================
# TEXT CHUNKING
# ======================================

def chunk_text(text, max_len=250):
    chunks = []
    if not text:
        return chunks

    text = str(text).strip()

    while len(text) > max_len:
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = text.rfind(" ", 0, max_len)
        if split_at == -1:
            split_at = max_len

        part = text[:split_at].strip()
        if part:
            chunks.append(part)

        text = text[split_at:].strip()

    if text:
        chunks.append(text)

    return chunks


# ======================================
# SPRACHE AUS REPORT ERKENNEN
# ======================================

def detect_language(insight):
    if isinstance(insight, str):
        match = re.search(r"\(([A-Z]{2})\)", insight)
        if match:
            return match.group(1).lower()

    return os.getenv("APP_LANG", "de")


# ======================================
# CLIENTS (v2 & v1.1)
# ======================================

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
        api_key, 
        api_secret, 
        access_token, 
        access_token_secret
    )
    api_v1 = tweepy.API(auth)

    return client_v2, api_v1


# ======================================
# X THREAD
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
        client, api_v1 = get_clients()

        if client is None or api_v1 is None:
            print("⚠️ X (Twitter) API Keys fehlen.")
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

        btc = global_crypto.get("bitcoin", {})
        eth = global_crypto.get("ethereum", {})
        dfi = market.get("dfi", {})

        btc_price = btc.get("price", "N/A")
        btc_change = safe_float(btc.get("change", 0))

        eth_price = eth.get("price", "N/A")
        eth_change = safe_float(eth.get("change", 0))

        dfi_price = dfi.get("price", dfi.get("usd", "N/A"))
        dfi_change = safe_float(dfi.get("change", 0))

        score = intelligence.get("total", "N/A")
        status = intelligence.get("status", "N/A")
        daily_insight = intelligence.get("daily_insight", "")

        flags = (
            "🇩🇪 🇬🇧 🇺🇸 🇸🇻 🇺🇾 🇧🇷 🇦🇷 "
            "🇳🇴 🇸🇪 🇫🇮 🇿🇦 🇦🇺 🇳🇿 "
            "🇨🇳 🇯🇵 🇮🇳 🇮🇩 🇫🇷 🇪🇸 "
            "🇵🇹 🇷🇺 🇸🇦"
        )

        header_title = lang.get("header_title", "🚀 DeFiChain Daily Intelligence")
        global_crypto_title = lang.get("global_crypto", "Global Crypto")
        intelligence_title = lang.get("intelligence", "🧠 Intelligence Score")
        price_title = lang.get("price", "Price")
        change_title = lang.get("change_24h", "24h")
        network_title = lang.get("network", "Network")
        news_title = lang.get("news", "News")
        history_title = lang.get("history", "History")

        # ==================================
        # TWEET 1
        # ==================================
        post1 = f"""
{header_title} ({language.upper()})

🌍 {flags}

🌍 {global_crypto_title}

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
            post1 = post1[:277] + "..."

        result1 = client.create_tweet(text=post1)
        tweet1_id = result1.data["id"]

        # ==================================
        # TWEET 2
        # ==================================
        post2 = f"""
🧠 {intelligence_title}

⭐ {score}/100
{status}

💡 Insight:

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
        # TWEET 3
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
        # TWEET 4
        # ==================================
        post4 = f"📚 {history_title}".strip()

        if current_history:
            history_id = current_history.get("id", "N/A")
            history_name = current_history.get("title", "DeFiChain Update")
            history_text = current_history.get(
                "text", 
                current_history.get("content", "")
            )

            post4 += (
                f"\n\nChapter {history_id}\n"
                f"{history_name}\n\n"
                f"{history_text[:140]}"
            )
        else:
            post4 += "\n\nDeFiChain ecosystem update."

        post4 += "\n\n#DeFiChain #DFI"

        if len(post4) > 280:
            post4 = post4[:277] + "..."

        result4 = client.create_tweet(
            text=post4,
            in_reply_to_tweet_id=tweet3_id
        )
        tweet4_id = result4.data["id"]

        # ==================================
        # TWEET 5: GIF VIA CHUNKED UPLOAD
        # ==================================
       try:
    image_path = "outputs/daily_update.png"

    if os.path.exists(image_path):
        # Statisches PNG-Bild für Twitter hochladen
        media = api_v1.media_upload(filename=image_path)

        post5 = "📊 Daily DeFiChain Update Visualized 🌐\n\n#DeFiChain #DFI"
        result5 = client.create_tweet(
            text=post5,
            media_ids=[media.media_id],
            in_reply_to_tweet_id=tweet4_id
        )
        print("X Tweet 5 (Bild) gesendet:", result5.data["id"], flush=True)
    else:
        print(f"⚠️ Bild nicht gefunden unter: {image_path}", flush=True)

except Exception as img_error:
    print("⚠️ Fehler beim Bild-Upload auf X:", img_error, flush=True)
