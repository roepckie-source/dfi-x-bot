import os
import tweepy


def get_twitter_client():
    """Initialisiert den Twitter API v2 Client über Environment Variables."""
    try:
        client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )
        return client
    except Exception as e:
        print(f"⚠️ Fehler beim Initialisieren des Twitter Clients: {e}")
        return None


def format_large_number(num):
    """Formatiert große Zahlen in kompakte Strings (z.B. 1.15B, 829.00M, 288.0K)."""
    if not isinstance(num, (int, float)):
        return "0"
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return f"{num:.2f}"


def send_x_thread(
    insight="",
    tokenomics=None,
    dusd=None,
    network=None,
    intelligence=None,
    global_crypto=None,
    market=None,
):
    """Erstellt und sendet einen sauberen 3-Tweet Thread an Twitter/X."""
    client = get_twitter_client()
    if not client:
        print("❌ Twitter Client nicht verfügbar. Abbruch.")
        return

    tokenomics = tokenomics or {}
    network = network or {}
    intelligence = intelligence or {}
    market = market or {}

    # ===================================================
    # METRIKEN AUFBEREITEN
    # ===================================================
    btc_price = market.get("btc_price", 0)
    btc_change = market.get("btc_change", 0)
    btc_signal = "🟢" if btc_change >= 0 else "🔴"

    eth_price = market.get("eth_price", 0)
    eth_change = market.get("eth_change", 0)
    eth_signal = "🟢" if eth_change >= 0 else "🔴"

    dfi_price = market.get("dfi_price", 0)
    dfi_change = market.get("dfi_change", 0)
    dfi_signal = "🟢" if dfi_change >= 0 else "🔴"

    total_sup = format_large_number(tokenomics.get("total_supply", 0))
    circ_sup = format_large_number(tokenomics.get("circulating_supply", 0))
    burned_dfi = format_large_number(tokenomics.get("burned_dfi", 0))
    daily_minted = format_large_number(tokenomics.get("daily_minted", 0))

    score = intelligence.get("score", 50)
    status = intelligence.get("status", "Neutral")
    daily_insight = intelligence.get(
        "insight", "Netzwerkdaten werden überwacht."
    )

    # ===================================================
    # TWEET 1: MAIN MARKET OVERVIEW
    # ===================================================
    post1 = f"""
🚀 DeFiChain Intelligence (EN)

🌍 BTC: ${btc_price:,.2f} ({btc_signal}{btc_change:.2f}%)
🌍 ETH: ${eth_price:,.2f} ({eth_signal}{eth_change:.2f}%)

💎 DFI: ${dfi_price:.6f} ({dfi_signal}{dfi_change:.2f}%)
📦 Total Supply: {total_sup} DFI
💧 Circulating: {circ_sup} DFI

#DeFiChain #DFI
""".strip()

    # Safety-Cutoff für Tweet 1
    if len(post1) > 280:
        post1 = post1[:277] + "..."

    try:
        result1 = client.create_tweet(text=post1)
        tweet1_id = result1.data["id"]
        print(f"✅ Tweet 1 erfolgreich gesendet! (ID: {tweet1_id})")
    except Exception as e:
        print(f"❌ Fehler beim Senden von Tweet 1: {e}")
        return

    # ===================================================
    # TWEET 2: ON-CHAIN TOKENOMICS & SHORT INSIGHT
    # ===================================================
    # Insight dynamisch kürzen, damit Tweet 2 nie > 280 Zeichen wird
    insight_snippet = (
        daily_insight
        if len(daily_insight) <= 100
        else daily_insight[:97] + "..."
    )

    post2 = f"""
🔥 Burned: {burned_dfi} DFI
🪙 Daily Minted: {daily_minted} DFI

🧠 Score: {score}/100 ({status})

💡 Daily Insight:
{insight_snippet}
""".strip()

    if len(post2) > 280:
        post2 = post2[:277] + "..."

    try:
        result2 = client.create_tweet(
            text=post2, in_reply_to_tweet_id=tweet1_id
        )
        tweet2_id = result2.data["id"]
        print(f"✅ Tweet 2 erfolgreich gesendet! (ID: {tweet2_id})")
    except Exception as e:
        print(f"❌ Fehler beim Senden von Tweet 2: {e}")
        return

    # ===================================================
    # TWEET 3: NETWORK STATUS & FULL DAILY NEWS
    # ===================================================
    network_status = network.get("network_status", "🟢 Online")
    news_text = insight if isinstance(insight, str) else ""

    # News dynamisch kürzen, um Platz für Header und Hashtag zu garantieren
    news_snippet = (
        news_text if len(news_text) <= 140 else news_text[:137] + "..."
    )

    post3 = f"""
⛓ Network: {network_status}

📰 Daily Update:
{news_snippet}

#DeFiChain
""".strip()

    if len(post3) > 280:
        post3 = post3[:277] + "..."

    try:
        client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)
        print("✅ Tweet 3 erfolgreich gesendet! Thread komplett.")
    except Exception as e:
        print(f"❌ Fehler beim Senden von Tweet 3: {e}")
