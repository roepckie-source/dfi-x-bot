# ============================================
# DeFiChain Intelligence v5
# X / Twitter Thread Output
# ============================================

import os
import time
import tweepy

from modules.language import load_language


# -------------------------------------------------
# Status-Übersetzungen
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


def change_emoji(value):
    value = safe_float(value)

    if value > 0:
        return "🟢"

    if value < 0:
        return "🔴"

    return "⚪"


def get_status_key(score):
    score = safe_float(score)

    if score >= 80:
        return "strong"

    if score >= 60:
        return "stable"

    if score >= 40:
        return "caution"

    return "critical"


def get_status(language, score):
    translations = STATUS_TRANSLATIONS.get(
        language,
        STATUS_TRANSLATIONS["en"]
    )

    return translations.get(
        get_status_key(score),
        "Stable"
    )


def get_intelligence_score(intelligence):
    """
    Liest den Score robust aus unterschiedlichen möglichen
    Strukturen des Intelligence-Moduls.
    """

    if intelligence is None:
        return 0

    # Falls direkt eine Zahl übergeben wurde
    if isinstance(intelligence, (int, float)):
        return intelligence

    if not isinstance(intelligence, dict):
        return 0

    possible_keys = [
        "score",
        "intelligence_score",
        "intelligenceScore",
        "index",
        "value",
        "rating",
        "total_score",
        "total",
    ]

    for key in possible_keys:
        value = intelligence.get(key)

        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                pass

    # Falls der Score verschachtelt ist
    for value in intelligence.values():

        if isinstance(value, dict):
            nested = get_intelligence_score(value)

            if nested != 0:
                return nested

    return 0


def detect_language(text):
    if not text:
        return "en"

    text = str(text)

    # Unser Report enthält z.B. "(ES)"
    import re

    match = re.search(
        r"\(([a-zA-Z]{2})\)",
        text
    )

    if match:
        return match.group(1).lower()

    return "en"


def get_news(insight):
    if not insight:
        return ""

    text = str(insight)

    markers = [
        "📰 News:",
        "📰 Noticias:",
        "📰 Actualités:",
        "📰 Новости:",
        "📰 ニュース:",
        "📰 Noticias:",
    ]

    for marker in markers:

        if marker in text:

            part = text.split(marker, 1)[1]

            if "📚" in part:
                part = part.split("📚", 1)[0]

            return part.strip()

    return ""


def get_history(insight, current_history=None):
    if insight:

        text = str(insight)

        markers = [
            "📚 History:",
            "📚 Historia:",
            "📚 Histoire:",
            "📚 Geschichte:",
            "📚 История:",
            "📚 歴史:",
        ]

        for marker in markers:

            if marker in text:
                return text.split(marker, 1)[1].strip()

    if isinstance(current_history, dict):

        return (
            current_history.get("title")
            or current_history.get("text")
            or current_history.get("content")
            or ""
        )

    if current_history:
        return str(current_history)

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


def limit_tweet(text, maximum=260):
    """
    Konservative Begrenzung.
    260 statt 280 gibt etwas Sicherheitsreserve,
    insbesondere wegen Emojis und X-Zeichenbewertung.
    """

    if not text:
        return ""

    text = str(text).strip()

    if len(text) <= maximum:
        return text

    return text[:maximum - 3].rstrip() + "..."


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

    language = detect_language(insight)

    lang = load_language(language)

    print(f"🌍 X Sprache: {language.upper()}")

    # -------------------------------------------------
    # Markt
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

    total_burn = safe_float(
        burn.get("total", 0)
    )

    address_burn = safe_float(
        burn.get("address", 0)
    )

    fees_burn = safe_float(
        burn.get("fees", 0)
    )

    auction_burn = safe_float(
        burn.get("auction", 0)
    )

    payback_burn = safe_float(
        burn.get("payback", 0)
    )

    emission = safe_float(
        tokenomics.get("emission", 0)
    )

    net_change = safe_float(
        tokenomics.get(
            "net_change",
            total_burn - emission
        )
    )

    # -------------------------------------------------
    # Intelligence
    # -------------------------------------------------

    score = get_intelligence_score(
        intelligence
    )

    status = get_status(
        language,
        score
    )

    print(
        f"🧠 X Intelligence Score: "
        f"{score}/100"
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
    # Netzwerk
    # -------------------------------------------------

    block = network.get(
        "block",
        network.get(
            "block_height",
            "N/A"
        )
    )

    masternodes = network.get(
        "masternodes",
        "N/A"
    )

    # -------------------------------------------------
    # Übersetzungen
    # -------------------------------------------------

    title = lang.get(
        "x_title_daily",
        lang.get(
            "header_title",
            "🚀 DeFiChain Daily"
        )
    )

    flags = lang.get(
        "header_line1",
        "🌍 🇩🇪 🇬🇧 🇺🇸 🇪🇸 🇵🇹 🇷🇺 🇯🇵 🇨🇳 🇮🇳 🇮🇩 🇫🇷 🇸🇦"
    )

    global_crypto_label = lang.get(
        "global_crypto",
        "Global Crypto"
    )

    price_label = lang.get(
        "price",
        "Price"
    )

    change_label = lang.get(
        "change",
        "Change"
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

    update_label = lang.get(
        "content_update",
        "Daily Update"
    )

    # -------------------------------------------------
    # Tweet 1 – Markt
    # -------------------------------------------------

    tweet1 = (
        f"{title} ({language.upper()})\n"
        f"{flags}\n\n"
        f"🌍 {global_crypto_label}\n"
        f"₿ Bitcoin: ${format_number(btc_price)} "
        f"{change_emoji(btc_change)} "
        f"{safe_float(btc_change):+.2f}%\n"
        f"Ξ Ethereum: ${format_number(eth_price)} "
        f"{change_emoji(eth_change)} "
        f"{safe_float(eth_change):+.2f}%\n\n"
        f"💎 DeFiChain DFI\n"
        f"{price_label}: {format_dfi_price(dfi_price)}\n"
        f"{change_label}: "
        f"{change_emoji(dfi_change)} "
        f"{safe_float(dfi_change):+.2f}%\n\n"
        f"#DeFiChain #DFI"
    )

    # -------------------------------------------------
    # Tweet 2 – Tokenomics + Intelligence
    # -------------------------------------------------

    tweet2 = (
        f"🔥 {tokenomics_label}\n"
        f"{burn_label}: {total_burn / 1_000_000:.2f}M DFI\n"
        f"{emission_label}: {emission / 1_000_000:.2f}M DFI\n"
        f"{net_burn_label}: {net_change / 1_000_000:.2f}M DFI\n"
        f"• Address: {address_burn / 1_000_000:.2f}M\n"
        f"• Fees: {fees_burn / 1_000:.2f}K\n"
        f"• Auction: {auction_burn / 1_000_000:.2f}M\n"
        f"• Payback: {payback_burn / 1_000_000:.2f}M\n\n"
        f"🧠 {intelligence_label}\n"
        f"{score_label}: {safe_float(score):.0f}/100\n"
        f"{status_label}: {status}"
    )

    # -------------------------------------------------
    # Tweet 3 – Network + dUSD
    # Bewusst kurz halten!
    # -------------------------------------------------

    tweet3 = (
        f"⛓ {network_label}\n"
        f"{block_label}: {block}\n"
        f"{masternodes_label}: {masternodes}\n\n"
        f"💵 {dusd_label}\n"
        f"{price_label}: ${dusd_price}\n"
        f"Health: {dusd_health}\n"
        f"Peg: {peg_difference}"
    )

    # -------------------------------------------------
    # Tweet 4 – Insight + News + History
    # -------------------------------------------------

    news_text = get_news(insight)
    history_text = get_history(
        insight,
        current_history
    )

    # Nur den eigentlichen Insight-Text extrahieren,
    # nicht den kompletten Report.
    insight_text = ""

    if insight:

        text = str(insight)

        if "💡 Insight:" in text:
            insight_text = text.split(
                "💡 Insight:",
                1
            )[1]

            if "📰" in insight_text:
                insight_text = insight_text.split(
                    "📰",
                    1
                )[0]

            if "📚" in insight_text:
                insight_text = insight_text.split(
                    "📚",
                    1
                )[0]

            insight_text = insight_text.strip()

    tweet4 = (
        f"💡 {insight_label}\n"
        f"{insight_text[:100] if insight_text else 'N/A'}\n\n"
        f"📰 {update_label}\n"
        f"{news_text[:80] if news_text else 'N/A'}\n\n"
        f"📚 {history_label}\n"
        f"{history_text[:70] if history_text else 'N/A'}"
    )

    # -------------------------------------------------
    # Sicherheitsbegrenzung
    # -------------------------------------------------

    tweets = [
        limit_tweet(tweet1, 260),
        limit_tweet(tweet2, 260),
        limit_tweet(tweet3, 260),
        limit_tweet(tweet4, 260),
    ]

    # -------------------------------------------------
    # Debug
    # -------------------------------------------------

    for index, text in enumerate(tweets, start=1):

        print()
        print(f"DEBUG Tweet {index}:")
        print(text)
        print(
            f"Zeichen: {len(text)}"
        )
        print("-" * 60)

    # -------------------------------------------------
    # Thread senden
    # -------------------------------------------------

    previous_tweet_id = None

    for index, text in enumerate(
        tweets,
        start=1
    ):

        try:

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
                f"✅ Tweet {index} "
                f"({language.upper()}) "
                f"gesendet: {tweet_id}"
            )

            if index < len(tweets):
                time.sleep(3)

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
