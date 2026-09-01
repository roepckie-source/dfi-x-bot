# ======================================
# DeFiChain Intelligence v5
# X Thread Bot (inkl. GIF Support)
# ======================================

import os
import re
import tweepy

from modules.language import load_language
from charts import create_smooth_fade_gif


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
    """
    Teilt längere Texte sauber an Zeilenumbrüchen
    oder Leerzeichen auf.
    """
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
    """
    Erkennt die Sprache aus dem Report.

    Beispiel:
    🚀 DeFiChain Intelligence (FR)
    """
    if isinstance(insight, str):
        match = re.search(r"\(([A-Z]{2})\)", insight)
        if match:
            return match.group(1).lower()

    # Fallback
    return os.getenv("APP_LANG", "de")


# ======================================
# CLIENTS (v2 & v1.1)
# ======================================

def get_clients():
    """
    Erstellt sowohl den Tweepy Client (v2) als auch 
    die Tweepy API (v1.1) für den Media Upload.
    """
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        return None, None

    # Client für Twitter API v2 (Tweets erstellen)
    client_v2 = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # API für Twitter API v1.1 (Media-Upload für GIFs/Bilder)
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

        # ==================================
        # CLIENTS INITIALISIEREN
        # ==================================

        client, api_v1 = get_clients()

        if client is None or api_v1 is None:
            print("⚠️ X (Twitter) API Keys fehlen.")
            return False

        # ==================================
        # SPRACHE
        # ==================================

        language = detect_language(insight)
        lang = load_language(language)

        # ==================================
        # FALLBACKS
        # ==================================

        if not isinstance(intelligence, dict):
            intelligence = {}

        if not isinstance(global_crypto, dict):
            global_crypto = {}

        if not isinstance(market, dict):
            market = {}

        if not isinstance(network, dict):
            network = {}

        # ==================================
        # MARKTDATEN
        # ==================================

        btc = global_crypto.get("bitcoin", {})
        eth = global_crypto.get("ethereum", {})
        dfi = market.get("dfi", {})

        # BTC
        btc_price = btc.get("price", "N/A")
        btc_change = safe_float(btc.get("change", 0))

        # ETH
        eth_price = eth.get("price", "N/A")
        eth_change = safe_float(eth.get("change", 0))

        # DFI
        dfi_price = dfi.get("price", dfi.get("usd", "N/A"))
        dfi_change = safe_float(dfi.get("change", 0))

        # INTELLIGENCE
        score = intelligence.get("total", "N/A")
        status = intelligence.get("status", "N/A")
        daily_insight = intelligence.get("daily_insight", "")

        # FLAGGENKETTE
        flags = (
            "🇩🇪 🇬🇧 🇺🇸 🇸🇻 🇺🇾 🇧🇷 🇦🇷 "
            "🇳🇴 🇸🇪 🇫🇮 🇿🇦 🇦🇺 🇳🇿 "
            "🇨🇳 🇯🇵 🇮🇳 🇮🇩 🇫🇷 🇪🇸 "
            "🇵🇹 🇷🇺 🇸🇦"
        )

        # SPRACH-TEXTE
        header_title = lang.get("header_title", "🚀 DeFiChain Daily Intelligence")
        global_crypto_title = lang.get("global_crypto", "Global Crypto")
        intelligence_title = lang.get("intelligence", "🧠 Intelligence Score")
        price_title = lang.get("price", "Price")
        change_title = lang.get("change_24h", "24h")
        network_title = lang.get("network", "Network")
        news_title = lang.get("news", "News")
        history_title = lang.get("history", "History")

        # ==================================
        # TWEET 1: GLOBAL CRYPTO + DFI
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

        print("DEBUG Tweet 1:\n", post1)

        result1 = client.create_tweet(text=post1)
        tweet1_id = result1.data["id"]
        print("X Tweet 1 gesendet:", tweet1_id)

        # ==================================
        # TWEET 2: INTELLIGENCE + INSIGHT
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

        print("DEBUG Tweet 2:\n", post2)

        result2 = client.create_tweet(
            text=post2,
            in_reply_to_tweet_id=tweet1_id
        )
        tweet2_id = result2.data["id"]
        print("X Tweet 2 gesendet:", tweet2_id)

        # ==================================
        # TWEET 3: NETWORK + NEWS
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

        print("DEBUG Tweet 3:\n", post3)

        result3 = client.create_tweet(
            text=post3,
            in_reply_to_tweet_id=tweet2_id
        )
        tweet3_id = result3.data["id"]
        print("X Tweet 3 gesendet:", tweet3_id)

        # ==================================
        # TWEET 4: HISTORY
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

        print("DEBUG Tweet 4:\n", post4)

        result4 = client.create_tweet(
            text=post4,
            in_reply_to_tweet_id=tweet3_id
        )
        tweet4_id = result4.data["id"]
        print("X Tweet 4 gesendet:", tweet4_id)

        # ==================================
        # TWEET 5: GIF UPDATE (VISUAL)
        # ==================================

        try:
            gif_output_path = "outputs/daily_update.gif"
            chart_files = [
                "outputs/chart1.png", 
                "outputs/chart2.png", 
                "outputs/summary.png"
            ]

            # 1. Animiertes GIF mit Transitions erstellen
            create_smooth_fade_gif(chart_files, output_gif_path=gif_output_path)

            # 2. GIF über Twitter v1.1 hochladen
            media = api_v1.media_upload(filename=gif_output_path)

            # 3. Als Tweet 5 (Antwort auf Tweet 4) senden
            post5 = "🎬 Daily DeFiChain Update Visualized 🌐\n\n#DeFiChain #DFI"
            result5 = client.create_tweet(
                text=post5,
                media_ids=[media.media_id],
                in_reply_to_tweet_id=tweet4_id
            )
            print("X Tweet 5 (GIF) gesendet:", result5.data["id"])

        except Exception as gif_error:
            print("⚠️ Fehler beim GIF-Upload:", gif_error)

        # ==================================
        # ERFOLG
        # ==================================

        print("🎉 X Thread erfolgreich gesendet!")
        return True

    except Exception as e:
        print("❌ Fehler beim Senden an X:")
        print(e)
        return False
