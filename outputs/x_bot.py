# ==============================================================
# DeFiChain X (Twitter) Bot Module - x_bot.py
# ==============================================================

import logging
import os
from datetime import datetime, timezone
import requests
import tweepy

# Importe aus deinen eigenen Repository-Modulen
try:
  from insights import get_daily_insight
except ImportError:

  def get_daily_insight(lang="de"):
    return "DeFiChain Netzwerk-Parameter und Tokenomics laufen stabil."


try:
  from news import get_daily_news
except ImportError:

  def get_daily_news(lang="de"):
    return "DeFiChain Ökosystem-Aktivitäten verlaufen wie geplant."


# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def safe_float(val, default=0.0):
  """Konvertiert Werte sicher in Float."""
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
  """Kürzt Text sauber an einer Wortgrenze, um das Limit nicht zu sprengen."""
  if not isinstance(text, str) or len(text) <= max_chars:
    return text or ""

  truncated = text[: max_chars - 3]
  if " " in truncated:
    truncated = truncated.rsplit(" ", 1)[0]
  return truncated + "..."


def get_twitter_client():
  """Initialisiert den Tweepy Client für X/Twitter API v2."""
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
        "⚠️ X API Keys fehlen in den Umgebungsvariablen. Versand übersprungen."
    )
    return None

  try:
    return tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
  except Exception as e:
    logging.error(f"❌ Fehler beim Tweepy-Client-Aufbau: {e}")
    return None


def post_x_thread_tweepy(
    dfi_data,
    btc_p,
    btc_c,
    eth_p,
    eth_c,
    lang_code="de",
    insight_text="",
    news_text="",
):
  """Erstellt und sendet einen 3-teiligen X-Thread mit strikter Einhaltung der 280-Zeichen-Grenze."""
  client = get_twitter_client()
  if not client:
    return

  lang_str = str(lang_code).upper()

  # Falls keine Texte übergeben wurden, lade sie aus deinen Repository-Modulen
  if not insight_text:
    try:
      insight_text = get_daily_insight(lang_code)
    except Exception:
      insight_text = "DeFiChain Netzwerk-Parameter und Tokenomics stabil."

  if not news_text:
    try:
      news_text = get_daily_news(lang_code)
    except Exception:
      news_text = "DeFiChain Ökosystem-Aktivitäten verlaufen regulär."

  # Marktdaten vorbereiten
  dfi_price = safe_float(dfi_data.get("price_usd"), 0.00278)
  dfi_change = safe_float(dfi_data.get("price_change_24h"), 0.0)
  dfi_sig = "🟢" if dfi_change >= 0 else "🔴"
  btc_sig = "🟢" if btc_c >= 0 else "🔴"
  eth_sig = "🟢" if eth_c >= 0 else "🔴"

  total_sup = format_large_number(dfi_data.get("total_supply", 1150000000))
  circ_sup = format_large_number(dfi_data.get("circulating_supply", 829000000))
  burned_dfi = format_large_number(dfi_data.get("burned_dfi", 412500000))
  daily_minted = format_large_number(dfi_data.get("daily_minted", 70300))

  # ------------------------------------------------------------------
  # TWEET 1: Marktübersicht (ca. 160 gewichtete Zeichen -> Absolut sicher)
  # ------------------------------------------------------------------
  post1 = (
      f"Crypto ({lang_str})\n\n"
      f"₿ BTC: ${btc_p:,.2f} ({btc_sig} {btc_c:.2f}%)\n"
      f"Ξ ETH: ${eth_p:,.2f} ({eth_sig} {eth_c:.2f}%)\n"
      f"💎 DFI: ${dfi_price:.6f} ({dfi_sig} {dfi_change:.2f}%)\n\n"
      f"📦 Total: {total_sup} DFI | 💧 Circ: {circ_sup} DFI\n\n"
      "#DeFiChain #DFI"
  )

  try:
    res1 = client.create_tweet(text=post1)
    tweet1_id = res1.data["id"]
    logging.info(
        f"✅ Tweepy: Tweet 1 ({lang_str}) erfolgreich gesendet! ID: {tweet1_id}"
    )
  except Exception as e:
    logging.error(f"❌ Tweepy: Fehler bei Tweet 1: {e}")
    return

  # ------------------------------------------------------------------
  # TWEET 2: Tokenomics + Daily Insight (max 120 Zeichen für Text -> Passt garantiert)
  # ------------------------------------------------------------------
  insight_clean = safe_truncate(insight_text, 120)
  post2 = (
      f"🔥 Burned: {burned_dfi} DFI\n"
      f"🪙 Minted: {daily_minted} DFI/Tag\n\n"
      f"🧠 Health: 67/100 (Stabil)\n\n"
      f"💡 Daily Insight:\n{insight_clean}"
  )

  try:
    res2 = client.create_tweet(text=post2, in_reply_to_tweet_id=tweet1_id)
    tweet2_id = res2.data["id"]
    logging.info("✅ Tweepy: Tweet 2 erfolgreich gesendet!")
  except Exception as e:
    logging.error(f"❌ Tweepy: Fehler bei Tweet 2: {e}")
    return

  # ------------------------------------------------------------------
  # TWEET 3: Netzwerk-Status + News aus dfi_news.json + Link
  # ------------------------------------------------------------------
  # Hinweis: URLs wie https://defilivescan.io zählen bei X starr als 23 Zeichen
  news_clean = safe_truncate(news_text, 110)
  post3 = (
      f"⛓ Network: 🟢 Online\n\n"
      f"📰 Daily News:\n{news_clean}\n\n"
      f"🔍 Live Scanner:\nhttps://defilivescan.io\n\n"
      "#DeFiChain"
  )

  try:
    client.create_tweet(text=post3, in_reply_to_tweet_id=tweet2_id)
    logging.info(
        f"✅ Tweepy: Tweet 3 erfolgreich gesendet! Thread ({lang_str})"
        " komplett."
    )
  except Exception as e:
    logging.error(f"❌ Tweepy: Fehler bei Tweet 3: {e}")


# Falls die Datei direkt zum Testen aufgerufen wird
if __name__ == "__main__":
  test_dfi = {
      "price_usd": 0.002781,
      "price_change_24h": 0.0,
      "burned_dfi": 412500000.0,
      "daily_minted": 70300.0,
      "total_supply": 1150000000.0,
      "circulating_supply": 829000000.0,
  }
  print("Starte lokalen Testlauf von x_bot.py...")
  post_x_thread_tweepy(
      test_dfi,
      80921.0,
      4.10,
      2510.55,
      4.42,
      lang_code="de",
      insight_text="Test Insight aus der Sprachdatei.",
      news_text="Test News aus dfi_news.json.",
  )
