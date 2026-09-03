# ======================================
# DeFiChain Intelligence v5
# X Thread Bot (Fully Fixed)
# ======================================

import os
import re
import tweepy
from modules.language import load_language


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
    val = float(value)
    if val <= 0:
      return "0.003000"  # Absicherung
    if val < 0.01:
      return f"{val:.8f}"
    if val < 1:
      return f"{val:.6f}"
    if val < 100:
      return f"{val:.2f}"
    return f"{val:,.2f}"
  except (TypeError, ValueError):
    return "0.003000"


def format_large_number(value, suffix=""):
  """Formatiert große Zahlen z. B. zu 412.50M oder 288.00K."""
  if value is None or value == "" or value == "N/A":
    return "N/A"

  try:
    val = float(str(value).replace(",", "").replace("DFI", "").strip())
  except (ValueError, TypeError):
    return "N/A"

  if val <= 0:
    return "N/A"

  if val >= 1_000_000_000:
    return f"{val / 1_000_000_000:.2f}B{suffix}"
  if val >= 1_000_000:
    return f"{val / 1_000_000:.2f}M{suffix}"
  if val >= 1_000:
    return f"{val / 1_000:.1f}K{suffix}"

  return f"{val:,.2f}{suffix}"


def change_emoji(value):
  try:
    return "🟢" if float(value) >= 0 else "🔴"
  except (TypeError, ValueError):
    return "⚪"


def detect_language(insight):
  if isinstance(insight, str):
    match = re.search(r"\(([A-Z]{2})\)", insight)
    if match:
      return match.group(1).lower()
  return os.getenv("APP_LANG", "de")


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
      access_token_secret=access_token_secret,
  )

  auth = tweepy.OAuth1UserHandler(
      api_key, api_secret, access_token, access_token_secret
  )
  api_v1 = tweepy.API(auth)

  return client_v2, api_v1


def send_x_thread(
    insight,
    tokenomics=None,
    dusd=None,
    network=None,
    intelligence=None,
    current_history=None,
    global_crypto=None,
    market=None,
):
  try:
    client, _ = get_clients()

    if client is None:
      print("⚠️ X (Twitter) API Keys fehlen.", flush=True)
      return False

    language = detect_language(insight)
    lang = load_language(language)

    intelligence = intelligence if isinstance(intelligence, dict) else {}
    global_crypto = global_crypto if isinstance(global_crypto, dict) else {}
    market = market if isinstance(market, dict) else {}
    network = network if isinstance(network, dict) else {}
    tokenomics = tokenomics if isinstance(tokenomics, dict) else {}

    # Markt-Daten extrahieren
    btc = global_crypto.get("bitcoin", {})
    eth = global_crypto.get("ethereum", {})
    dfi = market.get("dfi", {})

    btc_price = btc.get("price", 0)
    btc_change = safe_float(btc.get("change", 0))

    eth_price = eth.get("price", 0)
    eth_change = safe_float(eth.get("change", 0))

    dfi_price = dfi.get("price", 0)
    dfi_change = safe_float(dfi.get("change", 0))

    # Tokenomics auslesen
    burned_raw = tokenomics.get(
        "burned_dfi", tokenomics.get("burned", 412500000.0)
    )
    minted_raw = tokenomics.get(
        "daily_minted", tokenomics.get("minted", 288000.0)
    )

    burned_dfi = format_large_number(burned_raw)
    daily_minted = format_large_number(minted_raw)

    score = intelligence.get("total", 67)
    status = intelligence.get("status", "Stabil")
    daily_insight = intelligence.get("daily_insight", "")

    header_title = lang.get("header_title", "🚀 DeFiChain Daily Intelligence")

    # ==================================
    # TWEET 1: PREISE & TOKENOMICS
    # ==================================
    post1 = f"""
{header_title} ({language.upper()})

🌍 BTC: ${format_price(btc_price)} ({change_emoji(btc_change)}{safe_change(btc_change)}%)
🌍 ETH: ${format_price(eth_price)} ({change_emoji(eth_change)}{safe_change(eth_change)}%)

💎 DFI: ${format_price(dfi_price)} ({change_emoji(dfi_change)}{safe_change(dfi_change)}%)
🔥 Burned: {burned_dfi} DFI
🪙 Daily Minted: {daily_minted} DFI

🧠 Score: {score}/100 ({status})

#DeFiChain #DFI
""".strip()

    if len(post1) > 280:
      post1 = post1[:277] + "..."

    result1 = client.create_tweet(text=post1)
    tweet1_id = result1.data["id"]

    # ==================================
    # TWEET 2: INSIGHTS & SCORE
    # ==================================
    post2 = f"""
🧠 Score: {score}/100 ({status})

💡 Daily Insight:

{daily_insight}
""".strip()

    if len(post2) > 280:
      post2 = post2[:277] + "..."

    result2 = client.create_tweet(
        text=post2, in_reply_to_tweet_id=tweet1_id
    )
    tweet2_id = result2.data["id"]

    # ==================================
    # TWEET 3: NETWORK & NEWS
    # ==================================
    network_status = network.get("network_status", "🟢 Online")

    post3 = f"""
⛓ Network: {network_status}

📰 Daily Update
""".strip()

    if isinstance(insight, str) and len(insight) > 0:
      post3 += f"\n\n{insight[:180]}"

    if len(post3) > 280:
      post3 = post3[:277] + "..."

    client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)

    return True

  except Exception as e:
    print(f"❌ Fehler bei send_x_thread: {e}", flush=True)
    return False
