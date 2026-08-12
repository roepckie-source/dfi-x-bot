# ======================================
# DeFiChain Intelligence v5
# X Thread Bot (Ultra-Kompakt + Flaggen)
# ======================================

import os
import tweepy
from modules.language import load_language

# Flaggen-Mapping für unterstützte Sprachen & Regionen
FLAGS = {
    "en": "🇺🇸", "us": "🇺🇸",
    "de": "🇩🇪",
    "zh": "🇨🇳", "cn": "🇨🇳",
    "id": "🇮🇩",
    "hi": "🇮🇳", "in": "🇮🇳",
    "ru": "🇷🇺",
    "pt": "🇧🇷", "br": "🇧🇷",
    "tr": "🇹🇷",
    "global": "🌐", "world": "🌐"
}

# X API Zugang
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")


def get_client():
    return tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET
    )


def short_num(val):
    try:
        val = float(val)
        if val >= 1_000_000: return f"{val / 1_000_000:.2f}M"
        if val >= 1_000: return f"{val / 1_000:.2f}K"
        return f"{val:.2f}"
    except Exception:
        return "N/A"


def fmt_change(val):
    try:
        v = float(val)
        return f"{'🟢' if v >= 0 else '🔴'} {v:+.2f}%"
    except Exception:
        return "⚪ N/A"


def truncate(text, max_len=275):
    if len(text) <= max_len:
        return text
    return text[:max_len - 3].rsplit(' ', 1)[0] + "..."


def send_x_thread(
    market,
    tokenomics,
    dusd,
    network,
    intelligence,
    history=None,
    global_crypto=None,
    comparison=None,
    news=None,
    language="en"
):
    try:
        lang = load_language(language)
        client = get_client()

        # Flagge der aktuellen Sprache holen (Fallback auf 🌐)
        lang_flag = FLAGS.get(language.lower(), "🌐")

        dfi = market.get("dfi", {})
        btc = global_crypto.get("bitcoin", {}) if global_crypto else {}
        eth = global_crypto.get("ethereum", {}) if global_crypto else {}

        score = intelligence.get("total", "N/A")
        status = intelligence.get("status", "N/A")

        # ==================================
        # TWEET 1: Ultra-Kompakte Marktübersicht
        # ==================================
        post1 = f"""🚀 DeFiChain Daily {lang_flag}🌐

₿ BTC: ${btc.get('price', 'N/A')} ({fmt_change(btc.get('change'))})
Ξ ETH: ${eth.get('price', 'N/A')} ({fmt_change(eth.get('change'))})
💎 DFI: ${dfi.get('usd', 'N/A')} ({fmt_change(dfi.get('change'))})

🧠 Score: ⭐ {score}/100 ({status})

#DeFiChain #DFI #Crypto""".strip()

        post1 = truncate(post1)
        print("DEBUG Tweet 1:\n", post1)
        res1 = client.create_tweet(text=post1)
        tweet1_id = res1.data["id"]

        # ==================================
        # TWEET 2: Tokenomics & Netzwerk
        # ==================================
        net_burn = tokenomics.get("balance", 0)
        net_status = network.get("network_status", "Active")
        insight = intelligence.get("daily_insight", "Monitoring active")
        burn_emoji = "🟢" if float(net_burn) >= 0 else "🔴"

        post2 = f"""🔥 DFI Tokenomics & Network {lang_flag}

⚖️ Net Burn: {burn_emoji} {short_num(net_burn)} DFI
⛓️ Status: {net_status}

💡 Insight:
{insight}

#DeFiChain #DFI""".strip()

        post2 = truncate(post2)
        print("DEBUG Tweet 2:\n", post2)
        res2 = client.create_tweet(text=post2, in_reply_to_tweet_id=tweet1_id)
        tweet2_id = res2.data["id"]

        # ==================================
        # TWEET 3: Historie / Update
        # ==================================
        if history:
            c_id = history.get("id", "N/A")
            c_title = history.get("title", "Update")
            c_text = history.get("text", "")
            if len(c_text) > 120:
                c_text = c_text[:117].rsplit(' ', 1)[0] + "..."

            post3 = f"""📰 DFI History {lang_flag}

📚 Ch.{c_id}: {c_title}
"{c_text}"

#DeFiChain #DFI""".strip()
        else:
            post3 = f"""📰 DFI Update {lang_flag}

Ecosystem & DEX metrics actively monitored.

#DeFiChain #DFI""".strip()

        post3 = truncate(post3)
        print("DEBUG Tweet 3:\n", post3)
        client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)

        print("🎉 X Thread erfolgreich gesendet!")

    except Exception as e:
        print("⚠️ X Posting fehlgeschlagen:", e)
