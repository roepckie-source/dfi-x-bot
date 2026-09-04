import os
import tweepy


def get_twitter_client():
    """Initialisiert den Twitter Client mit automatischen Key-Fallbacks."""
    api_key = os.getenv("TWITTER_API_KEY") or os.getenv("X_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET") or os.getenv("X_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN") or os.getenv(
        "X_ACCESS_TOKEN"
    )
    access_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET") or os.getenv(
        "X_ACCESS_TOKEN_SECRET"
    )
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN") or os.getenv(
        "X_BEARER_TOKEN"
    )

    if not all([api_key, api_secret, access_token, access_secret]):
        print(
            "⚠️ X/Twitter Keys fehlen in der Umgebung. Tweet wird übersprungen."
        )
        return None

    try:
        return tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )
    except Exception as e:
        print(f"⚠️ Fehler beim Initialisieren des Twitter Clients: {e}")
        return None


def format_large_number(num):
    """Formatiert große Zahlen kompakt (z.B. 1.15B, 829.00M, 288.0K)."""
    if not isinstance(num, (int, float)):
        return "0"
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return f"{num:.2f}"


def safe_float(val, default=0.0):
    """Konvertiert Werte sicher in Float und fängt 0/None ab."""
    if val is None:
        return default
    try:
        res = float(val)
        return res if res > 0 else default
    except (ValueError, TypeError):
        return default


def safe_truncate(text: str, max_chars: int) -> str:
    """Kürzt Text an der letzten Wortgrenze vor max_chars."""
    if not isinstance(text, str) or len(text) <= max_chars:
        return text or ""

    truncated = text[: max_chars - 3]
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return truncated + "..."


def send_x_thread(
    insight="",
    tokenomics=None,
    dusd=None,
    network=None,
    intelligence=None,
    global_crypto=None,
    market=None,
    lang_code="DE",
):
    """Erstellt und sendet einen 3-Tweet Thread an Twitter/X mit DeFiLiveScan Link."""
    if isinstance(lang_code, dict):
        lang_str = str(lang_code.get("code", "DE")).upper()
    elif isinstance(lang_code, str):
        lang_str = lang_code.upper()
    else:
        lang_str = "DE"

    client = get_twitter_client()
    if not client:
        print("❌ Twitter Client nicht erreichbar oder Keys fehlen. Abbruch.")
        return

    tokenomics = tokenomics or {}
    network = network or {}
    intelligence = intelligence or {}
    market = market or {}

    # METRIKEN ABSICHERN
    btc_price = safe_float(market.get("btc_price"), 81145.00)
    btc_change = safe_float(market.get("btc_change"), 0.0)
    btc_signal = "🟢" if btc_change >= 0 else "🔴"

    eth_price = safe_float(market.get("eth_price"), 2495.84)
    eth_change = safe_float(market.get("eth_change"), 0.0)
    eth_signal = "🟢" if eth_change >= 0 else "🔴"

    dfi_price = safe_float(market.get("dfi_price"), 0.00304145)
    dfi_change = safe_float(market.get("dfi_change"), 0.0)
    dfi_signal = "🟢" if dfi_change >= 0 else "🔴"

    total_sup = format_large_number(
        safe_float(tokenomics.get("total_supply"), 1150000000.0)
    )
    circ_sup = format_large_number(
        safe_float(tokenomics.get("circulating_supply"), 829000000.0)
    )
    burned_dfi = format_large_number(
        safe_float(tokenomics.get("burned_dfi"), 412500000.0)
    )
    daily_minted = format_large_number(
        safe_float(tokenomics.get("daily_minted"), 288000.0)
    )

    score = intelligence.get("score", 67)
    status = intelligence.get("status", "Stabil")
    daily_insight = intelligence.get(
        "insight", "Netzwerkdaten werden überwacht."
    )

    # TWEET 1
    post1 = f"""
Crypto ({lang_str})

₿ Bitcoin:
${btc_price:,.2f}
{btc_signal} {btc_change:.2f}%

Ξ Ethereum:
${eth_price:,.2f}
{eth_signal} {eth_change:.2f}%

💎 DeFiChain DFI:
${dfi_price:.8f}
{dfi_signal} {dfi_change:.2f}%

📦 Total Supply: {total_sup} DFI
💧 Circulating: {circ_sup} DFI

#DeFiChain #DFI
""".strip()

    if len(post1) > 280:
        post1 = safe_truncate(post1, 280)

    try:
        result1 = client.create_tweet(text=post1)
        tweet1_id = result1.data["id"]
        print(f"✅ Tweet 1 ({lang_str}) erfolgreich gesendet!")
    except Exception as e:
        print(f"❌ Fehler beim Senden von Tweet 1: {e}")
        return

    # TWEET 2
    insight_snippet = safe_truncate(daily_insight, 90)
    post2 = f"""
🔥 Burned: {burned_dfi} DFI
🪙 Daily Minted: {daily_minted} DFI

🧠 Score: {score}/100 ({status})

💡 Daily Insight:
{insight_snippet}
""".strip()

    if len(post2) > 280:
        post2 = safe_truncate(post2, 280)

    try:
        result2 = client.create_tweet(
            text=post2, in_reply_to_tweet_id=tweet1_id
        )
        tweet2_id = result2.data["id"]
        print("✅ Tweet 2 erfolgreich gesendet!")
    except Exception as e:
        print(f"❌ Fehler beim Senden von Tweet 2: {e}")
        return

    # TWEET 3 (Mit DeFiLiveScan Link)
    network_status = network.get("network_status", "🟢 Online")
    news_text = insight if isinstance(insight, str) else ""
    news_snippet = safe_truncate(news_text, 100)

    post3 = f"""
⛓ Network: {network_status}

📰 Daily Update:
{news_snippet}

🔍 Live Data: https://defilivescan.io

#DeFiChain
""".strip()

    if len(post3) > 280:
        post3 = safe_truncate(post3, 280)

    try:
        client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)
        print(f"✅ Tweet 3 erfolgreich gesendet! Thread ({lang_str}) komplett.")
    except Exception as e:
        print(f"❌ Fehler beim Senden von Tweet 3: {e}")
