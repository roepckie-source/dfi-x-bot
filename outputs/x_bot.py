# ======================================
# DeFiChain Intelligence v5
# X Thread Bot (Alle Flaggen in Tweet 1)
# ======================================

import os
import tweepy
from modules.language import load_language

# Flaggen-Mapping für alle 10 Sprachdateien aus /languages
FLAGS = {
    "en": "🇺🇸",
    "de": "🇩🇪",
    "es": "🇪🇸",
    "fr": "🇫🇷",
    "pt": "🇧🇷",
    "ru": "🇷🇺",
    "ja": "🇯🇵",
    "hi": "🇮🇳",
    "id": "🇮🇩",
    "ar": "🇸🇦"
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
        if abs(val) >= 1_000_000:
            return f"{val / 1_000_000:.2f}M"
        if abs(val) >= 1_000:
            return f"{val / 1_000:.2f}K"
        return f"{val:.2f}"
    except Exception:
        return str(val) if val else "0.00"


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

        # Flagge der heutigen Sprache
        lang_flag = FLAGS.get(str(language).lower(), "🌐")

        # String mit allen 10 Flaggen nebeneinander
        all_flags = "".join(FLAGS.values())

        dfi = market.get("dfi", {}) if isinstance(market, dict) else {}
        btc = global_crypto.get("bitcoin", {}) if isinstance(global_crypto, dict) else {}
        eth = global_crypto.get("ethereum", {}) if isinstance(global_crypto, dict) else {}

        score = intelligence.get("total", "N/A") if isinstance(intelligence, dict) else "N/A"
        status = intelligence.get("status", "N/A") if isinstance(intelligence, dict) else "N/A"

        # ==================================
        # TWEET 1: Marktübersicht + Alle Flaggen
        # ==================================
        post1 = f"""🚀 DeFiChain Daily {lang_flag}

🌐 {all_flags}

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
        # TWEET 2: Tokenomics & Network
        # ==================================
        raw_burn = None
        if isinstance(tokenomics, dict):
            raw_burn = (
                tokenomics.get("net_burn")
                if tokenomics.get("net_burn") is not None
                else tokenomics.get("balance")
                if tokenomics.get("balance") is not None
                else tokenomics.get("burn")
            )

        if (raw_burn is None or raw_burn == 0) and isinstance(intelligence, dict):
            raw_burn = intelligence.get("net_burn", intelligence.get("burn", 0))

        if isinstance(raw_burn, dict):
            raw_burn = raw_burn.get("total", raw_burn.get("balance", 0))

        net_status = network.get("network_status", "Active") if isinstance(network, dict) else "Active"
        insight = intelligence.get("daily_insight", "Monitoring active") if isinstance(intelligence, dict) else "Monitoring active"

        try:
            burn_val = float(raw_burn)
            burn_emoji = "🟢" if burn_val >= 0 else "🔴"
        except (ValueError, TypeError):
            burn_emoji = "🟢"

        post2 = f"""🔥 DFI Tokenomics & Network {lang_flag}

⚖️ Net Burn: {burn_emoji} {short_num(raw_burn)} DFI
⛓️ Status: {net_status}

💡 Insight:
{insight}

#DeFiChain #DFI""".strip()

        post2 = truncate(post2)
        print("DEBUG Tweet 2:\n", post2)
        res2 = client.create_tweet(text=post2, in_reply_to_tweet_id=tweet1_id)
        tweet2_id = res2.data["id"]

        # ==================================
        # TWEET 3: DeFiChain History
        # ==================================
        if history and isinstance(history, dict):
            c_id = history.get("id", "")
            c_title = history.get("title", "Milestone")
            c_text = history.get("text", history.get("description", ""))
            c_date = history.get("date", history.get("year", ""))

            date_str = f" ({c_date})" if c_date else ""
            chap_str = f"Ch.{c_id}: " if c_id else ""

            if len(c_text) > 120:
                c_text = c_text[:117].rsplit(' ', 1)[0] + "..."

            post3 = f"""📰 DFI History {lang_flag}

📚 {chap_str}{c_title}{date_str}
"{c_text}"

#DeFiChain #DFI""".strip()

        else:
            post3 = f"""📰 DFI History {lang_flag}

📚 Native DeFi built on Bitcoin since 2019.
Decentralized financial applications empowering Bitcoin holders worldwide.

#DeFiChain #DFI""".strip()

        post3 = truncate(post3)
        print("DEBUG Tweet 3:\n", post3)
        client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)

        print("🎉 X Thread erfolgreich gesendet!")

    except Exception as e:
        print("⚠️ X Posting fehlgeschlagen:", e)
