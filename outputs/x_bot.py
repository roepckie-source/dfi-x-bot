# ==============================================================
# DeFiChain Daily Bot - x_bot.py (Tweepy API v2 Integration)
# ==============================================================

import os
import logging
from datetime import datetime
import tweepy

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def format_large_number(num):
    """Formatiert große Zahlen kompakt (z.B. 1.15B, 829.00M, 288.0K)."""
    try:
        val = float(num) if num is not None else 0.0
    except (ValueError, TypeError):
        val = 0.0

    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.2f}B"
    elif val >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    elif val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{val:.2f}"


def safe_truncate(text: str, max_chars: int) -> str:
    """Kürzt Text an der letzten Wortgrenze vor max_chars."""
    if not isinstance(text, str) or len(text) <= max_chars:
        return text or ""

    truncated = text[: max_chars - 3]
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return truncated + "..."


def get_twitter_client():
    """Initialisiert den Tweepy Twitter Client (v2 API)."""
    api_key = os.getenv("X_API_KEY") or os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("X_API_SECRET") or os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN") or os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        logging.warning("⚠️ X/Twitter API Keys fehlen in den Umgebungsvariablen.")
        return None

    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        return client
    except Exception as e:
        logging.error(f"❌ Fehler beim Initialisieren des Tweepy Clients: {e}")
        return None


def send_x_thread(
    insight,
    tokenomics,
    dusd,
    network,
    intelligence,
    global_crypto,
    market,
    lang_code="de",
):
    """
    Erstellt und sendet einen 3-teiligen X/Twitter-Thread über Tweepy.
    """
    client = get_twitter_client()
    if not client:
        return

    # 🛠️ Sichere Extraktion von lang_code (fängt Dict, String oder None ab)
    if isinstance(lang_code, dict):
        lang_str = str(lang_code.get("code") or lang_code.get("lang") or "de").upper()
    elif isinstance(lang_code, str):
        lang_str = lang_code.upper()
    else:
        lang_str = "DE"

    # Absicherung für Dictionaries
    global_crypto = global_crypto if isinstance(global_crypto, dict) else {}
    tokenomics = tokenomics if isinstance(tokenomics, dict) else {}
    intelligence = intelligence if isinstance(intelligence, dict) else {}
    network = network if isinstance(network, dict) else {}

    # Preissignale & Werte extrahieren
    btc_p = float(global_crypto.get("btc_price") or 0.0)
    btc_c = float(global_crypto.get("btc_change") or 0.0)
    eth_p = float(global_crypto.get("eth_price") or 0.0)
    eth_c = float(global_crypto.get("eth_change") or 0.0)
    dfi_p = float(global_crypto.get("dfi_price") or 0.0)
    dfi_c = float(global_crypto.get("dfi_change") or 0.0)

    btc_sig = "🟢" if btc_c >= 0 else "🔴"
    eth_sig = "🟢" if eth_c >= 0 else "🔴"
    dfi_sig = "🟢" if dfi_c >= 0 else "🔴"

    # Tokenomics Formatierung
    total_sup = format_large_number(tokenomics.get("total_supply", 0))
    circ_sup = format_large_number(tokenomics.get("circulating_supply", 0))
    burned_dfi = format_large_number(tokenomics.get("burned_dfi", 0))
    daily_minted = format_large_number(tokenomics.get("daily_minted", 0))

    # Intelligence & Network
    score = intelligence.get("score", 67)
    status_str = intelligence.get("status", "Stabil")
    net_status = network.get("network_status", "🟢 Online")

    # Timestamp verhindert "403 Duplicate Content" bei X
    timestamp_str = datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S UTC")

    # ===================================================
    # TWEET 1: MARKETS & SUPPLY
    # ===================================================
    post1 = f"""
Crypto ({lang_str}) · {timestamp_str}

₿ Bitcoin:
${btc_p:,.2f}
{btc_sig} {btc_c:.2f}%

Ξ Ethereum:
${eth_p:,.2f}
{eth_sig} {eth_c:.2f}%

💎 DeFiChain DFI:
${dfi_p:.8f}
{dfi_sig} {dfi_c:.2f}%

📦 Total: {total_sup} DFI | 💧 Circ: {circ_sup} DFI

#DeFiChain #DFI
""".strip()

    if len(post1) > 280:
        post1 = safe_truncate(post1, 280)

    try:
        res1 = client.create_tweet(text=post1)
        tweet1_id = res1.data["id"]
        logging.info(f"✅ Tweet 1 ({lang_str}) erfolgreich gesendet! ID: {tweet1_id}")
    except Exception as e:
        logging.error(f"❌ Fehler beim Senden von Tweet 1: {e}")
        return

    # ===================================================
    # TWEET 2: TOKENOMICS & INTELLIGENCE
    # ===================================================
    insight_text = insight if isinstance(insight, str) else "Netzwerkdaten werden überwacht."
    insight_snippet = safe_truncate(insight_text, 90)

    post2 = f"""
🔥 Burned: {burned_dfi} DFI
🪙 Daily Minted: {daily_minted} DFI

🧠 Score: {score}/100 (🟡 {status_str})

💡 Daily Insight:
{insight_snippet}
""".strip()

    if len(post2) > 280:
        post2 = safe_truncate(post2, 280)

    try:
        res2 = client.create_tweet(text=post2, in_reply_to_tweet_id=tweet1_id)
        tweet2_id = res2.data["id"]
        logging.info("✅ Tweet 2 erfolgreich gesendet!")
    except Exception as e:
        logging.error(f"❌ Fehler beim Senden von Tweet 2: {e}")
        return

    # ===================================================
    # TWEET 3: NETWORK STATUS & DEFILIVESCAN LINK
    # ===================================================
    news_snippet = safe_truncate(insight_text, 90)
    post3 = f"""
⛓ Network: {net_status}

📰 Daily Update:
{news_snippet}

🔍 Live Data:
https://defilivescan.io

#DeFiChain
""".strip()

    if len(post3) > 280:
        post3 = safe_truncate(post3, 280)

    try:
        client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)
        logging.info(f"✅ Tweet 3 erfolgreich gesendet! Thread ({lang_str}) komplett.")
    except Exception as e:
        logging.error(f"❌ Fehler beim Senden von Tweet 3: {e}")
