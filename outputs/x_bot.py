# ============================================
# DeFiChain Intelligence v5
# X / Twitter Thread Output
# ============================================

import os
import re
import time

import tweepy

from modules.language import load_language


# -------------------------------------------------
# Sprachabhängige Statuswerte
# -------------------------------------------------

STATUS_TRANSLATIONS = {
    "en": {
        "strong": "Strong",
        "stable": "Stable",
        "caution": "Caution",
        "critical": "Critical",
    },
    "de": {
        "strong": "Sehr stark",
        "stable": "Stabil",
        "caution": "Vorsicht",
        "critical": "Kritisch",
    },
    "es": {
        "strong": "Muy fuerte",
        "stable": "Estable",
        "caution": "Precaución",
        "critical": "Crítico",
    },
    "fr": {
        "strong": "Très fort",
        "stable": "Stable",
        "caution": "Prudence",
        "critical": "Critique",
    },
    "pt": {
        "strong": "Muito forte",
        "stable": "Estável",
        "caution": "Cuidado",
        "critical": "Crítico",
    },
    "ru": {
        "strong": "Очень сильный",
        "stable": "Стабильно",
        "caution": "Осторожно",
        "critical": "Критично",
    },
    "ja": {
        "strong": "非常に強い",
        "stable": "安定",
        "caution": "注意",
        "critical": "危険",
    },
    "zh": {
        "strong": "非常强劲",
        "stable": "稳定",
        "caution": "谨慎",
        "critical": "严重",
    },
    "hi": {
        "strong": "बहुत मजबूत",
        "stable": "स्थिर",
        "caution": "सावधानी",
        "critical": "गंभीर",
    },
    "id": {
        "strong": "Sangat kuat",
        "stable": "Stabil",
        "caution": "Hati-hati",
        "critical": "Kritis",
    },
    "ar": {
        "strong": "قوي جدًا",
        "stable": "مستقر",
        "caution": "حذر",
        "critical": "حرج",
    },
}


# -------------------------------------------------
# Hilfsfunktionen
# -------------------------------------------------

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def format_number(value, decimals=2):
    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def format_dfi_price(value):
    try:
        return f"${float(value):.8f}"
    except (TypeError, ValueError):
        return "N/A"


def get_status_key(score):
    score = safe_float(score)

    if score >= 80:
        return "strong"

    if score >= 60:
        return "stable"

    if score >= 40:
        return "caution"

    return "critical"


def get_localized_status(language, score, fallback=None):
    status_key = get_status_key(score)

    translations = STATUS_TRANSLATIONS.get(
        language,
        STATUS_TRANSLATIONS["en"]
    )

    return translations.get(
        status_key,
        fallback or status_key.title()
    )


def detect_language_from_text(text):
    if not text:
        return "en"

    match = re.search(
        r"\(([a-zA-Z]{2})\)",
        str(text)
    )

    if match:
        return match.group(1).lower()

    return "en"


def get_change_emoji(change):
    change = safe_float(change)

    if change > 0:
        return "🟢"

    if change < 0:
        return "🔴"

    return "⚪"


def extract_news(insight):
    if not insight:
        return ""

    text = str(insight)

    # Unterstützt unseren aktuellen Report
    patterns = [
        r"📰\s*News:\s*(.*?)(?=\n\n📚|\Z)",
        r"📰\s*Noticias:\s*(.*?)(?=\n\n📚|\Z)",
        r"📰\s*Actualités:\s*(.*?)(?=\n\n📚|\Z)",
        r"📰\s*Новости:\s*(.*?)(?=\n\n📚|\Z)",
        r"📰\s*ニュース:\s*(.*?)(?=\n\n📚|\Z)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.DOTALL
        )

        if match:
            return match.group(1).strip()

    return ""


def extract_history(insight):
    if not insight:
        return ""

    text = str(insight)

    patterns = [
        r"📚\s*History:\s*(.*)$",
        r"📚\s*Historia:\s*(.*)$",
        r"📚\s*Histoire:\s*(.*)$",
        r"📚\s*Geschichte:\s*(.*)$",
        r"📚\s*История:\s*(.*)$",
        r"📚\s*歴史:\s*(.*)$",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.DOTALL
        )

        if match:
            return match.group(1).strip()

    return ""


def create_client():
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
        print("❌ X API Zugangsdaten fehlen.")
        return None

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )


# -------------------------------------------------
# X Thread
# -------------------------------------------------

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

    print("=" * 60)
    print("🐦 X THREAD")
    print("=" * 60)

    client = create_client()

    if client is None:
        return False

    tokenomics = tokenomics or {}
    dusd = dusd or {}
    network = network or {}
    intelligence = intelligence or {}
    global_crypto = global_crypto or {}
    market = market or {}

    # -------------------------------------------------
    # Sprache bestimmen
    # -------------------------------------------------

    language = detect_language_from_text(insight)

    lang = load_language(language)

    print(f"🌍 X Sprache: {language.upper()}")

    # -------------------------------------------------
    # Market
    # -------------------------------------------------

    dfi = market.get("dfi", {})

    if not isinstance(dfi, dict):
        dfi = {}

    dfi_price = dfi.get(
        "usd",
        market.get("price", "N/A")
    )

    dfi_change = dfi.get(
        "change",
        market.get("change_24h", 0)
    )

    btc = global_crypto.get(
        "bitcoin",
        {}
    )

    eth = global_crypto.get(
        "ethereum",
        {}
    )

    btc_price = btc.get("price", "N/A")
    btc_change = btc.get("change", 0)

    eth_price = eth.get("price", "N/A")
    eth_change = eth.get("change", 0)

    # -------------------------------------------------
    # Tokenomics
    # -------------------------------------------------

    burn = tokenomics.get("burn", {})

    if not isinstance(burn, dict):
        burn = {}

    total_burn = burn.get(
        "total",
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

    emission = tokenomics.get(
        "emission",
        0
    )

    net_change = tokenomics.get(
        "net_change",
        total_burn - safe_float(emission)
    )

    # -------------------------------------------------
    # Intelligence
    # -------------------------------------------------

    score = intelligence.get(
        "score",
        intelligence.get("intelligence_score", 0)
    )

    status = get_localized_status(
        language,
        score
    )

    # -------------------------------------------------
    # dUSD
    # -------------------------------------------------

    dusd_price = dusd.get(
        "price",
        "N/A"
    )

    dusd_health = dusd.get(
        "health_score",
        "N/A"
    )

    peg_difference = dusd.get(
        "peg_difference",
        "N/A"
    )

    # -------------------------------------------------
    # Network
    # -------------------------------------------------

    block = network.get(
        "block",
        network.get("block_height", "N/A")
    )

    masternodes = network.get(
        "masternodes",
        "N/A"
    )

    # -------------------------------------------------
    # News / History
    # -------------------------------------------------

    news_text = extract_news(insight)

    if not news_text:
        news_text = lang.get(
            "content_update",
            "Daily DeFiChain update"
        )

    history_text = extract_history(insight)

    if not history_text and current_history:
        if isinstance(current_history, dict):
            history_text = (
                current_history.get("title")
                or current_history.get("text")
                or current_history.get("content")
                or ""
            )
        else:
            history_text = str(current_history)

    # -------------------------------------------------
    # Übersetzte Labels
    # -------------------------------------------------

    market_label = lang.get(
        "market",
        "Market"
    )

    price_label = lang.get(
        "price",
        "Price"
    )

    change_label = lang.get(
        "change",
        "Change"
    )

    global_crypto_label = lang.get(
        "global_crypto",
        "Global Crypto"
    )

    tokenomics_label = lang.get(
        "tokenomics",
        "Tokenomics"
    )

    burn_label = lang.get(
        "burn",
        "Burn"
    )

    emission_label = lang.get(
        "emission",
        "Emission"
    )

    net_burn_label = lang.get(
        "net_burn",
        "Net Burn"
    )

    intelligence_label = lang.get(
        "intelligence",
        "DFI Intelligence Index"
    )

    score_label = lang.get(
        "score",
        "Score"
    )

    status_label = lang.get(
        "status",
        "Status"
    )

    network_label = lang.get(
        "network",
        "Network"
    )

    block_label = lang.get(
        "block",
        "Block Height"
    )

    masternodes_label = lang.get(
        "masternodes",
        "Masternodes"
    )

    dusd_label = lang.get(
        "dusd_health",
        "dUSD Health"
    )

    insight_label = lang.get(
        "insight",
        "Daily Insight"
    )

    history_label = lang.get(
        "history",
        "DeFiChain History"
    )

    # -------------------------------------------------
    # Flaggenkette
    # -------------------------------------------------

    flags = lang.get(
        "header_line1",
        "🌍 🇩🇪 🇬🇧 🇺🇸 🇪🇸 🇵🇹 🇷🇺 🇯🇵 🇨🇳 🇮🇳 🇮🇩 🇫🇷 🇸🇦"
    )

    # -------------------------------------------------
    # Tweet 1
    # -------------------------------------------------

    title = lang.get(
        "x_title_daily",
        lang.get(
            "header_title",
            "🚀 DeFiChain Daily"
        )
    )

    tweet1 = (
        f"{title} ({language.upper()})\n"
        f"{flags}\n\n"
        f"🌍 {global_crypto_label}\n"
        f"₿ Bitcoin: ${format_number(btc_price)} "
        f"{get_change_emoji(btc_change)} "
        f"{safe_float(btc_change):+.2f}%\n"
        f"Ξ Ethereum: ${format_number(eth_price)} "
        f"{get_change_emoji(eth_change)} "
        f"{safe_float(eth_change):+.2f}%\n\n"
        f"💎 DeFiChain DFI\n"
        f"{price_label}: {format_dfi_price(dfi_price)}\n"
        f"{change_label}: "
        f"{get_change_emoji(dfi_change)} "
        f"{safe_float(dfi_change):+.2f}%\n\n"
        f"#DeFiChain #DFI"
    )

    # -------------------------------------------------
    # Tweet 2
    # -------------------------------------------------

    tweet2 = (
        f"🔥 {tokenomics_label}\n\n"
        f"{burn_label}: {safe_float(total_burn) / 1_000_000:.2f}M DFI\n"
        f"{emission_label}: {safe_float(emission) / 1_000_000:.2f}M DFI\n"
        f"{net_burn_label}: "
        f"{safe_float(net_change) / 1_000_000:.2f}M DFI\n\n"
        f"• Address: {safe_float(address_burn) / 1_000_000:.2f}M\n"
        f"• Fees: {safe_float(fees_burn) / 1_000:.2f}K\n"
        f"• Auction: {safe_float(auction_burn) / 1_000_000:.2f}M\n"
        f"• Payback: {safe_float(payback_burn) / 1_000_000:.2f}M\n\n"
        f"🧠 {intelligence_label}:\n"
        f"{score_label}: {score}/100\n"
        f"{status_label}: {status}"
    )

    # -------------------------------------------------
    # Tweet 3
    # -------------------------------------------------

    tweet3 = (
        f"⛓ {network_label}\n"
        f"{block_label}: {block}\n"
        f"{masternodes_label}: {masternodes}\n\n"
        f"💵 {dusd_label}\n"
        f"{price_label}: ${dusd_price}\n"
        f"Health: {dusd_health}\n"
        f"Peg: {peg_difference}\n\n"
        f"💡 {insight_label}:\n"
        f"{insight[:450] if insight else 'N/A'}"
    )

    # -------------------------------------------------
    # Tweet 4
    # -------------------------------------------------

    tweet4 = (
        f"📰 {lang.get('content_update', 'Daily Update')}\n\n"
        f"{news_text[:500]}\n\n"
        f"📚 {history_label}\n"
        f"{history_text[:350] if history_text else 'N/A'}"
    )

    tweets = [
        tweet1,
        tweet2,
        tweet3,
        tweet4
    ]

    # -------------------------------------------------
    # Thread senden
    # -------------------------------------------------

    previous_tweet_id = None

    for index, text in enumerate(tweets, start=1):

        try:

            print()
            print(f"DEBUG Tweet {index}:")
            print(text)
            print("-" * 60)

            if previous_tweet_id is None:

                result = client.create_tweet(
                    text=text
                )

            else:

                result = client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=previous_tweet_id
                )

            tweet_id = result.data["id"]

            previous_tweet_id = tweet_id

            print(
                f"✅ Tweet {index} ({language.upper()}) "
                f"gesendet: {tweet_id}"
            )

            # Kleine Pause zwischen den Tweets
            if index < len(tweets):
                time.sleep(2)

        except Exception as e:

            print(
                f"❌ Fehler bei Tweet {index}:"
            )

            print(
                type(e).__name__,
                str(e)
            )

            return False

    print()
    print("=" * 60)
    print("✅ X THREAD KOMPLETT GESENDET")
    print("=" * 60)

    return True
