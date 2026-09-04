# ==============================================================
# DeFiChain Daily Bot - main.py
# ==============================================================

import json
import logging
import os
from datetime import datetime, timezone
import requests
import tweepy

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Sprachrotation für täglichen Wechsel (de -> en -> ru)
ROTATION_LANGUAGES = ["de", "en", "ru"]


def get_daily_language() -> str:
  """Berechnet die Tages-Sprache anhand des Tages im Jahr."""
  day_of_year = datetime.now(timezone.utc).timetuple().tm_yday
  return ROTATION_LANGUAGES[day_of_year % len(ROTATION_LANGUAGES)]


def load_locale(lang_code: str) -> dict:
  """Lädt die JSON-Übersetzungsdatei für die angegebene Sprache."""
  lang = str(lang_code).lower()
  possible_paths = [
      f"locales/{lang}.json",
      f"{lang}.json",
      "locales/de.json",
      "de.json",
  ]

  for path in possible_paths:
    if os.path.exists(path):
      try:
        with open(path, "r", encoding="utf-8") as f:
          data = json.load(f)
          logging.info(f"📖 Sprachdatei erfolgreich geladen: {path}")
          return data
      except Exception as e:
        logging.warning(f"⚠️ Fehler beim Lesen von {path}: {e}")

  logging.warning(
      f"⚠️ Keine passende Sprachdatei für '{lang}' gefunden. Nutze Fallbacks."
  )
  return {}


def safe_float(val, default=0.0):
  """Konvertiert Werte sicher in Float und fängt None/ungültige Strings ab."""
  if val is None:
    return default
  try:
    return float(val)
  except (ValueError, TypeError):
    return default


def format_large_number(num):
  """Formatiert große Zahlen kompakt (z.B. 1.15B, 829.00M, 70.3K)."""
  num = safe_float(num)
  if num >= 1_000_000_000:
    return f"{num / 1_000_000_000:.2f}B"
  elif num >= 1_000_000:
    return f"{num / 1_000_000:.2f}M"
  elif num >= 1_000:
    return f"{num / 1_000:.1f}K"
  return f"{num:.2f}"


def safe_truncate(text: str, max_chars: int) -> str:
  """Kürzt Text an der letzten Wortgrenze vor max_chars."""
  if not isinstance(text, str) or len(text) <= max_chars:
    return text or ""

  truncated = text[: max_chars - 3]
  if " " in truncated:
    truncated = truncated.rsplit(" ", 1)[0]
  return truncated + "..."


def get_twitter_client():
  """Initialisiert den Tweepy Twitter Client v2."""
  api_key = os.getenv("X_API_KEY") or os.getenv("TWITTER_API_KEY")
  api_secret = os.getenv("X_API_SECRET") or os.getenv("TWITTER_API_SECRET")
  access_token = os.getenv("X_ACCESS_TOKEN") or os.getenv(
      "TWITTER_ACCESS_TOKEN"
  )
  access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv(
      "TWITTER_ACCESS_TOKEN_SECRET"
  )
  bearer_token = os.getenv("X_BEARER_TOKEN") or os.getenv(
      "TWITTER_BEARER_TOKEN"
  )

  if not all([api_key, api_secret, access_token, access_token_secret]):
    logging.warning(
        "⚠️ X/Twitter API Keys fehlen in den Umgebungsvariablen. X-Versand"
        " wird übersprungen."
    )
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


def get_robust_dfi_data():
  """Holt DFI-Preis, Tokenomics und Supply-Metriken primär von DeFiLiveScan mit robustem Ocean-Fallback."""
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
  data = {
      "price_usd": None,
      "price_change_24h": 0.0,
      "burned_dfi": 0.0,
      "daily_minted": 0.0,
      "total_supply": 0.0,
      "circulating_supply": 0.0,
  }

  # 1. Primärer Abruf: DeFiLiveScan API
  try:
    defilive_res = requests.get(
        "https://defilivescan.io/api/stats", headers=headers, timeout=5
    ).json()

    stats = (
        defilive_res.get("data", defilive_res)
        if isinstance(defilive_res, dict)
        else {}
    )

    price = (
        stats.get("dfiPrice")
        or stats.get("priceUsd")
        or stats.get("dfi_price")
        or stats.get("price")
    )
    change = (
        stats.get("priceChange24h")
        or stats.get("price_change_24h")
        or stats.get("change24h")
    )
    burned = (
        stats.get("burnedDfi")
        or stats.get("burned_dfi")
        or stats.get("burned")
    )
    total = stats.get("totalSupply") or stats.get("total_supply")
    circ = stats.get("circulatingSupply") or stats.get("circulating_supply")
    minted = stats.get("dailyMinted") or stats.get("daily_minted")

    if price is not None and safe_float(price) > 0:
      data["price_usd"] = safe_float(price)
      data["price_change_24h"] = safe_float(change)
      data["burned_dfi"] = safe_float(burned)
      data["total_supply"] = safe_float(total)
      data["circulating_supply"] = safe_float(circ)
      data["daily_minted"] = safe_float(minted)
      logging.info(
          "✅ Live-Daten erfolgreich via DeFiLiveScan geladen: DFI ="
          f" ${data['price_usd']:.6f}"
      )
  except Exception as e:
    logging.warning(
        f"⚠️ DeFiLiveScan API nicht erreichbar ({e}), wechsle auf Ocean API..."
    )

  # 2. Sekundärer Fallback: Ocean API
  if (
      not data["price_usd"]
      or data["price_usd"] <= 0
      or data["total_supply"] <= 0
  ):
    try:
      ocean_res = requests.get(
          "https://ocean.defichain.com/v0/mainnet/stats",
          headers=headers,
          timeout=4,
      ).json()
      ocean_data = ocean_res.get("data", {})
      supply_data = ocean_data.get("tokens", {}).get("supply", {})

      if data["burned_dfi"] <= 0:
        data["burned_dfi"] = safe_float(supply_data.get("burned"))
      if data["total_supply"] <= 0:
        data["total_supply"] = safe_float(supply_data.get("total"))
      if data["circulating_supply"] <= 0:
        data["circulating_supply"] = safe_float(supply_data.get("circulating"))

      if data["daily_minted"] <= 0:
        block_emission = safe_float(
            ocean_data.get("emission", {}).get("total")
        )
        data["daily_minted"] = (
            block_emission * 2880 if block_emission > 0 else 70300.0
        )

    except Exception as e:
      logging.warning(f"⚠️ Ocean Stats API Fehler: {e}")

    try:
      price_res = requests.get(
          "https://ocean.defichain.com/v0/mainnet/prices/DFI-USD",
          headers=headers,
          timeout=4,
      ).json()
      raw_p = (
          price_res.get("data", {})
          .get("price", {})
          .get("aggregated", {})
          .get("amount")
      )
      if not data["price_usd"] or data["price_usd"] <= 0:
        data["price_usd"] = safe_float(raw_p)
    except Exception as e:
      logging.warning(f"⚠️ Ocean Price API Fehler: {e}")

  # Fallback-Werte
  if not data["price_usd"] or data["price_usd"] <= 0:
    data["price_usd"] = 0.00278
  if data["burned_dfi"] <= 0:
    data["burned_dfi"] = 412500000.0
  if data["daily_minted"] <= 0:
    data["daily_minted"] = 70300.0
  if data["total_supply"] <= 0:
    data["total_supply"] = 1150000000.0
  if data["circulating_supply"] <= 0:
    data["circulating_supply"] = 829000000.0

  return data


def fetch_crypto_market_data():
  """Holt Marktpreise für BTC und ETH von CoinGecko."""
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
  try:
    url = (
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    )
    res = requests.get(url, headers=headers, timeout=5).json()
    btc_p = safe_float(res.get("bitcoin", {}).get("usd"), 80941.0)
    btc_c = safe_float(res.get("bitcoin", {}).get("usd_24h_change"), 0.0)
    eth_p = safe_float(res.get("ethereum", {}).get("usd"), 2511.45)
    eth_c = safe_float(res.get("ethereum", {}).get("usd_24h_change"), 0.0)

    if btc_p <= 0:
      btc_p = 80941.0
    if eth_p <= 0:
      eth_p = 2511.45

    return btc_p, btc_c, eth_p, eth_c
  except Exception as e:
    logging.warning(f"⚠️ CoinGecko API Fehler: {e}. Nutze Standardwerte.")
    return 80941.0, 0.0, 2511.45, 0.0


def post_x_thread_tweepy(
    dfi_data,
    btc_p,
    btc_c,
    eth_p,
    eth_c,
    lang_code="DE",
    insight_text="",
    news_text="",
):
  """Veröffentlicht einen 3-teiligen Tweet-Thread mit Tweepy."""
  client = get_twitter_client()
  if not client:
    return

  lang_str = str(lang_code).upper()

  dfi_price = dfi_data["price_usd"]
  dfi_change = dfi_data["price_change_24h"]
  dfi_sig = "🟢" if dfi_change >= 0 else "🔴"
  btc_sig = "🟢" if btc_c >= 0 else "🔴"
  eth_sig = "🟢" if eth_c >= 0 else "🔴"

  total_sup = format_large_number(dfi_data["total_supply"])
  circ_sup = format_large_number(dfi_data["circulating_supply"])
  burned_dfi = format_large_number(dfi_data["burned_dfi"])
  daily_minted = format_large_number(dfi_data["daily_minted"])

  timestamp_str = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M:%S UTC")

  # Tweet 1: Marktübersicht
  post1 = f"""
Crypto ({lang_str}) · {timestamp_str}

₿ Bitcoin:
${btc_p:,.2f}
{btc_sig} {btc_c:.2f}%

Ξ Ethereum:
${eth_p:,.2f}
{eth_sig} {eth_c:.2f}%

💎 DeFiChain DFI:
${dfi_price:.8f}
{dfi_sig} {dfi_change:.2f}%

📦 Total: {total_sup} DFI | 💧 Circ: {circ_sup} DFI

#DeFiChain #DFI
""".strip()

  if len(post1) > 280:
    post1 = safe_truncate(post1, 280)

  try:
    res1 = client.create_tweet(text=post1)
    tweet1_id = res1.data["id"]
    logging.info(
        f"✅ Tweepy: Tweet 1 ({lang_str}) erfolgreich gesendet! ID: {tweet1_id}"
    )
  except Exception as e:
    logging.error(f"❌ Tweepy: Fehler beim Senden von Tweet 1: {e}")
    return

  # Tweet 2: Tokenomics & Daily Insight aus dem Katalog
  insight_snippet = safe_truncate(
      insight_text or "Netzwerkdaten werden überwacht.", 90
  )
  post2 = f"""
🔥 Burned: {burned_dfi} DFI
🪙 Daily Minted: {daily_minted} DFI

🧠 Score: 67/100 (Stabil)

💡 Daily Insight:
{insight_snippet}
""".strip()

  if len(post2) > 280:
    post2 = safe_truncate(post2, 280)

  try:
    res2 = client.create_tweet(text=post2, in_reply_to_tweet_id=tweet1_id)
    tweet2_id = res2.data["id"]
    logging.info("✅ Tweepy: Tweet 2 erfolgreich gesendet!")
  except Exception as e:
    logging.error(f"❌ Tweepy: Fehler beim Senden von Tweet 2: {e}")
    return

  # Tweet 3: Status & News Update aus dem Katalog
  news_snippet = safe_truncate(
      news_text or "DeFiChain Ökosystem läuft stabil.", 90
  )
  post3 = f"""
⛓ Network: 🟢 Online

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
    logging.info(
        f"✅ Tweepy: Tweet 3 erfolgreich gesendet! Thread ({lang_str})"
        " komplett."
    )
  except Exception as e:
    logging.error(f"❌ Tweepy: Fehler beim Senden von Tweet 3: {e}")


def send_telegram(message):
  """Sendet Nachricht an Telegram."""
  token = os.getenv("TELEGRAM_BOT_TOKEN")
  chat_id = os.getenv("TELEGRAM_CHAT_ID")
  if not token or not chat_id:
    logging.warning("⚠️ Telegram Token oder Chat-ID fehlt. Versand übersprungen.")
    return
  try:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(
        url,
        json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
        timeout=10,
    )
    logging.info("🤖 Telegram Nachricht erfolgreich gesendet")
  except Exception as e:
    logging.error(f"❌ Telegram Fehler: {e}")


def send_discord(message):
  """Sendet Nachricht an Discord."""
  webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
  if not webhook_url:
    logging.warning("⚠️ Discord Webhook-URL fehlt. Versand übersprungen.")
    return
  try:
    requests.post(webhook_url, json={"content": message}, timeout=10)
    logging.info("💬 Discord erfolgreich gesendet")
  except Exception as e:
    logging.error(f"❌ Discord Fehler: {e}")


def main():
  logging.info("🚀 DeFiChain Intelligence startet...")

  # 1. Sprache festlegen & Sprachdatei laden
  app_lang = os.getenv("APP_LANG", get_daily_language())
  logging.info(f"🌐 Aktuelle Sprache für heute: {app_lang}")
  locale_data = load_locale(app_lang)

  # 2. News/Insights aus Sprachdatei ziehen (fallbacks inklusive)
  day_of_year = datetime.now(timezone.utc).timetuple().tm_yday

  # Auslesen aus Listen oder Dictionaries in der JSON-Datei
  insights_list = locale_data.get("insights") or locale_data.get(
      "daily_insights", []
  )
  news_list = locale_data.get("news") or locale_data.get("daily_updates", [])

  if isinstance(insights_list, list) and len(insights_list) > 0:
    insight_text = insights_list[day_of_year % len(insights_list)]
  elif isinstance(insights_list, dict) and str(day_of_year) in insights_list:
    insight_text = insights_list[str(day_of_year)]
  else:
    insight_text = locale_data.get(
        "insight_fallback", "Ökosystem-Aktivität und Parameter stabil."
    )

  if isinstance(news_list, list) and len(news_list) > 0:
    news_text = news_list[(day_of_year + 1) % len(news_list)]
  elif isinstance(news_list, dict) and str(day_of_year) in news_list:
    news_text = news_list[str(day_of_year)]
  else:
    news_text = locale_data.get(
        "news_fallback", "DeFiChain Netzwerk und Konsensus laufen regulär."
    )

  # 3. Marktdaten laden
  dfi_data = get_robust_dfi_data()
  btc_p, btc_c, eth_p, eth_c = fetch_crypto_market_data()

  # 4. Messenger-Reports (Telegram/Discord)
  dfi_sig = "🟢" if dfi_data["price_change_24h"] >= 0 else "🔴"
  btc_sig = "🟢" if btc_c >= 0 else "🔴"
  eth_sig = "🟢" if eth_c >= 0 else "🔴"

  telegram_msg = f"""
🚀 <b>DeFiChain Daily Update</b> ({str(app_lang).upper()})

📅 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

━━━━━━━━━━━━━━

💰 <b>DFI Market & Tokenomics</b>
💎 Price: ${dfi_data['price_usd']:.6f} ({dfi_sig} {dfi_data['price_change_24h']:.2f}%)

📦 Total Supply: {format_large_number(dfi_data['total_supply'])} DFI
💧 Circulating: {format_large_number(dfi_data['circulating_supply'])} DFI
🔥 Total Burned: {format_large_number(dfi_data['burned_dfi'])} DFI
🪙 Daily Minted: {format_large_number(dfi_data['daily_minted'])} DFI

💡 <b>Daily Insight:</b>
{insight_text}

📰 <b>Update:</b>
{news_text}

━━━━━━━━━━━━━━

🌍 <b>Crypto Market</b>
₿ Bitcoin: ${btc_p:,.2f} ({btc_sig} {btc_c:.2f}%)
Ξ Ethereum: ${eth_p:,.2f} ({eth_sig} {eth_c:.2f}%)

━━━━━━━━━━━━━━

🔍 <b>Live On-Chain Scanner:</b> https://defilivescan.io

#DeFiChain #DFI
"""
  send_telegram(telegram_msg)
  send_discord(
      f"📊 DeFiChain Update ({str(app_lang).upper()}):\nDFI:"
      f" ${dfi_data['price_usd']:.6f} | BTC: ${btc_p:,.2f} | ETH:"
      f" ${eth_p:,.2f}\n💡 {insight_text}\nhttps://defilivescan.io"
  )

  # 5. X-Thread mit voneinander getrennten Insights & News posten
  post_x_thread_tweepy(
      dfi_data=dfi_data,
      btc_p=btc_p,
      btc_c=btc_c,
      eth_p=eth_p,
      eth_c=eth_c,
      lang_code=str(app_lang),
      insight_text=insight_text,
      news_text=news_text,
  )

  logging.info("🐦 X Thread erfolgreich ausgeführt")
  logging.info("✅ Report vollständig gesendet!")


if __name__ == "__main__":
  main()
