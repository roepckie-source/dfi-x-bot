# ======================================
# DeFiChain Intelligence v5
# X / Twitter Bot Output (Language-Aware)
# ======================================

import os
import tweepy
from modules.language import load_language


def get_x_api():
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("⚠️ X API Credentials fehlen!")
        return None

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )
        return client
    except Exception as e:
        print("❌ X API Verbindungsfehler:", e)
        return None


def send_x_thread(
    market,
    tokenomics,
    dusd,
    network,
    intelligence,
    current_history,
    global_crypto,
    comparison,
    news=None,
    language="de",
    lang_data=None,
):
    # Falls lang_data nicht übergeben wurde, selbst laden
    if not lang_data:
        lang_data = load_language(language)

    # Dynamic Übersetzungen aus lang_data (mit Fallbacks)
    title_daily = lang_data.get("x_title_daily", "🚀 DeFiChain Daily")
    title_tokenomics = lang_data.get("x_title_tokenomics", "🔥 DFI Tokenomics & Network")
    title_history = lang_data.get("x_title_history", "📰 DFI History")
    
    lbl_score = lang_data.get("score_title", "Score")
    lbl_burn = lang_data.get("net_burn", "Net Burn")
    lbl_status = lang_data.get("status", "Status")
    lbl_insight = lang_data.get("insight_title", "Insight")
    lbl_monitoring = lang_data.get("monitoring_active", "Monitoring active")

    # --------------------------------------------------
    # Tweet 1: Market & Intelligence
    # --------------------------------------------------
    btc_price = global_crypto.get("bitcoin", {}).get("price", "N/A")
    btc_change = global_crypto.get("bitcoin", {}).get("change", 0)
    btc_emoji = "🟢" if btc_change >= 0 else "🔴"

    eth_price = global_crypto.get("ethereum", {}).get("price", "N/A")
    eth_change = global_crypto.get("ethereum", {}).get("change", 0)
    eth_emoji = "🟢" if eth_change >= 0 else "🔴"

    dfi_raw = market.get("dfi", {})
    dfi_data = dfi_raw.get("dfi", {}) if isinstance(dfi_raw, dict) and "dfi" in dfi_raw else dfi_raw

    dfi_price = (
        dfi_data.get("price")
        or dfi_data.get("price_usd")
        or dfi_data.get("usd")
        or dfi_data.get("last_price")
        or "N/A"
    )
    dfi_change = dfi_data.get("change", 0) if isinstance(dfi_data, dict) else 0
    dfi_emoji = "🟢" if dfi_change >= 0 else "🔴"

    score = intelligence.get("total", 0)
    status = intelligence.get("status", "N/A")

    flag_map = {
        "de": "🇩🇪", "en": "🇺🇸", "ru": "🇷🇺", "es": "🇪🇸",
        "fr": "🇫🇷", "br": "🇧🇷", "jp": "🇯🇵", "in": "🇮🇳",
        "id": "🇮🇩", "sa": "🇸🇦"
    }
    lang_flag = flag_map.get(language, "🌐")

    tweet1 = f"{title_daily} {lang_flag}\n\n"
    tweet1 += "🌐 🇺🇸🇩🇪🇪🇸🇫🇷🇧🇷🇷🇺🇯🇵🇮🇳🇮🇩🇸🇦\n\n"
    tweet1 += f"₿ BTC: ${btc_price} ({btc_emoji} {btc_change:+.2f}%)\n"
    tweet1 += f"Ξ ETH: ${eth_price} ({eth_emoji} {eth_change:+.2f}%)\n"
    tweet1 += f"💎 DFI: ${dfi_price} ({dfi_emoji} {dfi_change:+.2f}%)\n\n"
    tweet1 += f"🧠 {lbl_score}: ⭐ {score}/100 ({status})\n\n"
    tweet1 += "#DeFiChain #DFI #Crypto"

    # --------------------------------------------------
    # Tweet 2: Tokenomics & Network
    # --------------------------------------------------
    raw_burn = tokenomics.get("burn", {}).get("total", 0)
    try:
        net_burn = f"{float(raw_burn) / 1_000_000:.2f}M"
    except (ValueError, TypeError):
        net_burn = str(raw_burn)

    net_status = network.get("network_status", "🟢 Online")

    tweet2 = f"{title_tokenomics} {lang_flag}\n\n"
    tweet2 += f"⚖️ {lbl_burn}: {net_burn} DFI\n"
    tweet2 += f"⛓️ {lbl_status}: {net_status}\n\n"
    tweet2 += f"💡 {lbl_insight}:\n{lbl_monitoring}\n\n"
    tweet2 += "#DeFiChain #DFI"

    # --------------------------------------------------
    # Tweet 3: History Chapter
    # --------------------------------------------------
    hist_title = "N/A"
    hist_text = ""
    hist_id = ""

    if current_history and isinstance(current_history, dict):
        hist_title = current_history.get("title", "N/A")
        hist_text = (
            current_history.get("content")
            or current_history.get("text")
            or current_history.get("description")
            or ""
        )
        hist_id = current_history.get("id", "")

    if len(hist_text) > 180:
        hist_text = hist_text[:177] + "..."

    tweet3 = f"{title_history} {lang_flag}\n\n"
    if hist_id:
        tweet3 += f"📚 Ch.{hist_id}: {hist_title}\n"
    else:
        tweet3 += f"📚 {hist_title}\n"

    if hist_text:
        tweet3 += f'"{hist_text}"\n\n'
    tweet3 += "#DeFiChain #DFI"

    # --------------------------------------------------
    # Tweets senden
    # --------------------------------------------------
    client = get_x_api()
    if client:
        try:
            res1 = client.create_tweet(text=tweet1)
            tweet_id = res1.data["id"]

            res2 = client.create_tweet(text=tweet2, in_reply_to_tweet_id=tweet_id)
            tweet_id = res2.data["id"]

            client.create_tweet(text=tweet3, in_reply_to_tweet_id=tweet_id)

            print("🎉 X Thread erfolgreich gesendet!")
        except Exception as e:
            print("❌ Fehler beim Senden des X Threads:", e)
    else:
        print("⚠️ X Bot im Dry-Run (keine API Tokens gesetzt).")
