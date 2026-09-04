# ==============================================================
# DeFiChain Bot - X (Twitter) Publisher Module (outputs/x_bot.py)
# ==============================================================

import logging
import os
import tweepy

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================================================
# HILFSFUNKTIONEN FÜR FORMATIERUNG
# ==============================================================
def format_large_number(val, is_de=True):
  """Formatiert große Zahlen übersichtlich mit Mio. / M Suffix."""
  try:
    val_num = float(val)
    if val_num >= 1e6:
      mio_val = val_num / 1e6
      suffix = " Mio." if is_de else "M"
      return f"{mio_val:,.2f}{suffix}"
    return f"{val_num:,.2f}"
  except (ValueError, TypeError):
    return "N/A"


def clean_text(text, max_len=180):
  """Kürzt lange Texte sauber ab und vermeidet abgeschnittene Wörter."""
  if not text:
    return ""
  text = text.replace("\n", " ").strip()
  if len(text) <= max_len:
    return text
  return text[: max_len - 3].rsplit(" ", 1)[0] + "..."


# ==============================================================
# HAUPTFUNKTION: X THREAD ERSTELLEN & POSTEN
# ==============================================================
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
  """Erstellt einen 3-teiligen X-Thread über Tweepy Client API v2."""
  is_de = lang_code.lower() == "de"

  # API Keys aus GitHub Secrets / Umgebungsvariablen laden
  api_key = os.getenv("X_API_KEY")
  api_secret = os.getenv("X_API_SECRET")
  access_token = os.getenv("X_ACCESS_TOKEN")
  access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

  if not all([api_key, api_secret, access_token, access_token_secret]):
    logging.warning("⚠️ X API Credentials fehlen. Posting übersprungen.")
    return

  # Tweepy Client v2 initialisieren
  try:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
  except Exception as e:
    logging.error(f"❌ Fehler bei der Initialisierung des X Clients: {e}")
    return

  # Indikatoren (🟢/🔴) für Marktpreise
  dfi_sig = "🟢" if dfi_data.get("price_change_24h", 0) >= 0 else "🔴"
  btc_sig = "🟢" if btc_c >= 0 else "🔴"
  eth_sig = "🟢" if eth_c >= 0 else "🔴"

  # Total Supply Skalierung (rechnet Rohwerte in Millionen um, falls nötig)
  raw_total = dfi_data.get("total_supply", 0)
  total_val = raw_total * 1e6 if raw_total < 1000000 else raw_total

  # Formatierte Strings für Supply-Werte
  max_supply_str = "1,20 Mrd." if is_de else "1.20B"
  total_str = format_large_number(total_val, is_de)
  circ_str = format_large_number(dfi_data.get("circulating_supply", 0), is_de)
  burned_str = format_large_number(dfi_data.get("burned_dfi", 0), is_de)

  # ------------------------------------------------------------
  # TWEET 1: Markt, Preise & Tokenomics (inkl. 1.2B Max Cap)
  # ------------------------------------------------------------
  header = "📊 Daily Update"
  lbl_gesamt = "Gesamt" if is_de else "Total"
  lbl_auflage = "Auflage" if is_de else "Circ"
  lbl_max = "Max" if is_de else "Max"

  tweet_1 = f"""{header} ({lang_code.upper()})

₿ BTC: ${btc_p:,.2f} ({btc_sig} {btc_c:.2f}%)
Ξ ETH: ${eth_p:,.2f} ({eth_sig} {eth_c:.2f}%)
💎 DFI: ${dfi_data.get('price_usd', 0):.6f} ({dfi_sig} {dfi_data.get('price_change_24h', 0):.2f}%)

🔒 {lbl_max}: {max_supply_str} DFI
📦 {lbl_gesamt}: {total_str} DFI | 💧 {lbl_auflage}: {circ_str} DFI
#DeFiChain #DFI"""

  # ------------------------------------------------------------
  # TWEET 2: Burn, Mint & Daily Insight
  # ------------------------------------------------------------
  lbl_burned = "Verbrannt" if is_de else "Burned"
  lbl_mint = "Prägung" if is_de else "Minted"
  lbl_day = "Tag" if is_de else "day"
  lbl_health = "Gesundheit" if is_de else "Health"
  lbl_insight = "Tägliche Einblicke" if is_de else "Daily Insights"

  short_insight = clean_text(insight_text, max_len=140)

  tweet_2 = f"""🔥 {lbl_burned}: {burned_str} DFI
🪙 {lbl_mint}: {dfi_data.get('daily_minted', 70300)/1000:.1f}K DFI/{lbl_day}

🧠 {lbl_health}: 67/100 (Stabil)

💡 {lbl_insight}:
{short_insight}"""

  # ------------------------------------------------------------
  # TWEET 3: Netzwerke & 100-Tage Daily News
  # ------------------------------------------------------------
  lbl_net = "Netzwerk" if is_de else "Network"
  lbl_news = "Tägliche Nachrichten" if is_de else "Daily News"
  lbl_scan = "Live-Scanner" if is_de else "Live Scanner"

  tweet_3 = f"""⛓ {lbl_net}: 🟢 Online

📰 {lbl_news}:
{news_text}

🔍 {lbl_scan}: https://defiscan.live
#DeFiChain"""

  # ------------------------------------------------------------
  # THREAD POSTEN (SEQUENTIELL)
  # ------------------------------------------------------------
  try:
    # Tweet 1 senden
    res1 = client.create_tweet(text=tweet_1)
    tweet_1_id = res1.data["id"]
    logging.info(f"✅ Tweepy: Tweet 1 gesendet! ID: {tweet_1_id}")

    # Tweet 2 als Antwort auf Tweet 1
    res2 = client.create_tweet(
        text=tweet_2, in_reply_to_tweet_id=tweet_1_id
    )
    tweet_2_id = res2.data["id"]
    logging.info("✅ Tweepy: Tweet 2 gesendet!")

    # Tweet 3 als Antwort auf Tweet 2
    res3 = client.create_tweet(
        text=tweet_3, in_reply_to_tweet_id=tweet_2_id
    )
    logging.info(
        f"✅ Tweepy: Tweet 3 gesendet! Thread ({lang_code.upper()})"
        " komplett."
    )

  except Exception as e:
    logging.error(f"❌ Fehler beim Versenden des X-Threads: {e}")
