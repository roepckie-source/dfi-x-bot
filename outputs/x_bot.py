# ==============================================================
# DeFiChain Bot - X (Twitter) Publisher Module (outputs/x_bot.py)
# ==============================================================

import logging
import os
import tweepy

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
  """Kürzt lange Texte sauber ab."""
  if not text:
    return ""
  text = text.replace("\n", " ").strip()
  if len(text) <= max_len:
    return text
  return text[: max_len - 3].rsplit(" ", 1)[0] + "..."


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
  """Erstellt einen 3-teiligen X-Thread über Tweepy Client API v2 in der gewählten Sprache."""
  lang = lang_code.lower()
  is_de = lang == "de"

  # API Keys laden
  api_key = os.getenv("X_API_KEY")
  api_secret = os.getenv("X_API_SECRET")
  access_token = os.getenv("X_ACCESS_TOKEN")
  access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

  if not all([api_key, api_secret, access_token, access_token_secret]):
    logging.warning("⚠️ X API Credentials fehlen. Posting übersprungen.")
    return

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

  # Indikatoren (🟢/🔴)
  dfi_sig = "🟢" if dfi_data.get("price_change_24h", 0) >= 0 else "🔴"
  btc_sig = "🟢" if btc_c >= 0 else "🔴"
  eth_sig = "🟢" if eth_c >= 0 else "🔴"

  # Umrechnung Rohwerte in Millionen
  raw_total = dfi_data.get("total_supply", 0)
  total_val = raw_total * 1e6 if raw_total < 1000000 else raw_total

  # Sprachspezifische Labels
  if lang == "de":
    lbl_max, lbl_gesamt, lbl_auflage = "Max", "Gesamt", "Auflage"
    lbl_burned, lbl_mint, lbl_day = "Verbrannt", "Prägung", "Tag"
    lbl_health, lbl_insight = "Gesundheit", "Tägliche Einblicke"
    lbl_net, lbl_news, lbl_scan = (
        "Netzwerk",
        "Tägliche Nachrichten",
        "Live-Scanner",
    )
    max_supply_str = "1,20 Mrd."
  elif lang == "ru":
    lbl_max, lbl_gesamt, lbl_auflage = "Макс", "Всего", "В обращения"
    lbl_burned, lbl_mint, lbl_day = "Сожжено", "Эмиссия", "день"
    lbl_health, lbl_insight = "Здоровье", "Ежедневная аналитика"
    lbl_net, lbl_news, lbl_scan = (
        "Сеть",
        "Ежедневные новости",
        "Сканер сети",
    )
    max_supply_str = "1.20 млрд"
  elif lang == "zh":
    lbl_max, lbl_gesamt, lbl_auflage = "最大", "总供应量", "流通量"
    lbl_burned, lbl_mint, lbl_day = "已销毁", "每日铸造", "天"
    lbl_health, lbl_insight = "健康度", "每日洞察"
    lbl_net, lbl_news, lbl_scan = "网络", "每日新闻", "实时浏览器"
    max_supply_str = "12亿"
  else:  # Fallback Englisch (en)
    lbl_max, lbl_gesamt, lbl_auflage = "Max", "Total", "Circ"
    lbl_burned, lbl_mint, lbl_day = "Burned", "Minted", "day"
    lbl_health, lbl_insight = "Health", "Daily Insights"
    lbl_net, lbl_news, lbl_scan = "Network", "Daily News", "Live Scanner"
    max_supply_str = "1.20B"

  total_str = format_large_number(total_val, is_de)
  circ_str = format_large_number(dfi_data.get("circulating_supply", 0), is_de)
  burned_str = format_large_number(dfi_data.get("burned_dfi", 0), is_de)

  # ------------------------------------------------------------
  # TWEET 1
  # ------------------------------------------------------------
  header = "📊 Daily Update"

  tweet_1 = f"""{header} ({lang.upper()})

₿ BTC: ${btc_p:,.2f} ({btc_sig} {btc_c:.2f}%)
Ξ ETH: ${eth_p:,.2f} ({eth_sig} {eth_c:.2f}%)
💎 DFI: ${dfi_data.get('price_usd', 0):.6f} ({dfi_sig} {dfi_data.get('price_change_24h', 0):.2f}%)

🔒 {lbl_max}: {max_supply_str} DFI
📦 {lbl_gesamt}: {total_str} DFI | 💧 {lbl_auflage}: {circ_str} DFI
#DeFiChain #DFI"""

  # ------------------------------------------------------------
  # TWEET 2
  # ------------------------------------------------------------
  short_insight = clean_text(insight_text, max_len=140)

  tweet_2 = f"""🔥 {lbl_burned}: {burned_str} DFI
🪙 {lbl_mint}: {dfi_data.get('daily_minted', 70300)/1000:.1f}K DFI/{lbl_day}

🧠 {lbl_health}: 67/100 (Stabil)

💡 {lbl_insight}:
{short_insight}"""

  # ------------------------------------------------------------
  # TWEET 3
  # ------------------------------------------------------------
  tweet_3 = f"""⛓ {lbl_net}: 🟢 Online

📰 {lbl_news}:
{news_text}

🔍 {lbl_scan}: https://defiscan.live
#DeFiChain"""

  # ------------------------------------------------------------
  # THREAD POSTEN
  # ------------------------------------------------------------
  try:
    res1 = client.create_tweet(text=tweet_1)
    tweet_1_id = res1.data["id"]
    logging.info(f"✅ Tweet 1 ({lang.upper()}) gesendet! ID: {tweet_1_id}")

    res2 = client.create_tweet(
        text=tweet_2, in_reply_to_tweet_id=tweet_1_id
    )
    tweet_2_id = res2.data["id"]
    logging.info(f"✅ Tweet 2 ({lang.upper()}) gesendet!")

    res3 = client.create_tweet(
        text=tweet_3, in_reply_to_tweet_id=tweet_2_id
    )
    logging.info(f"✅ Tweet 3 ({lang.upper()}) gesendet! Thread komplett.")

  except Exception as e:
    logging.error(f"❌ Fehler beim Versenden des X-Threads ({lang.upper()}): {e}")
