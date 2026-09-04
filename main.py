# ==============================================================
# DeFiChain Bot Main Orchestrator - main.py
# ==============================================================

from datetime import datetime, timezone
import json
import logging
import os
import sys
import requests

# Setze Arbeitsverzeichnis auf das Hauptverzeichnis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Modul-Importe aus deinem Repository
from insights import get_daily_insight
from news import get_dfi_news
from outputs.x_bot import post_x_thread_tweepy

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# API Endpunkte
OCEAN_API_URL = "https://ocean.defichain.com/v0/mainnet"
CG_API_URL = "https://api.coingecko.com/api/v3/simple/price"


# ==============================================================
# 1. API DATA FETCHING
# ==============================================================
def fetch_market_data():
  """Holt DFI-Statistiken über Ocean API sowie BTC & ETH Daten über CoinGecko."""
  logging.info("📡 Starte API-Abfragen...")

  # Default/Fallback-Werte für DFI
  dfi_data = {
      "price_usd": 0.00278,
      "price_change_24h": 0.0,
      "total_supply": 1150000000.0,
      "circulating_supply": 829000000.0,
      "burned_dfi": 412500000.0,
      "daily_minted": 70300.0,
  }

  # 1. DeFiChain Ocean API
  try:
    stats_res = (
        requests.get(f"{OCEAN_API_URL}/stats", timeout=10)
        .json()
        .get("data", {})
    )

    # Sicheres Parsing der Ocean API Datenstrukturen
    count_data = stats_res.get("count", {})
    if isinstance(count_data, dict):
      dfi_data["total_supply"] = float(count_data.get("tokens", 1150000000))
    elif isinstance(count_data, (int, float)):
      dfi_data["total_supply"] = float(count_data)

    burned_data = stats_res.get("burned", {})
    if isinstance(burned_data, dict):
      dfi_data["burned_dfi"] = float(burned_data.get("total", 412500000))

    # DFI Preis aus Ocean API Token-Pair holen
    prices_res = (
        requests.get(f"{OCEAN_API_URL}/prices", timeout=10)
        .json()
        .get("data", [])
    )
    for t in prices_res:
      if t.get("currency") == "USDT":
        dfi_data["price_usd"] = float(
            t.get("price", {}).get("aggregated", 0.00278)
        )
        break

    logging.info("✅ Ocean API Daten erfolgreich erfasst.")
  except Exception as e:
    logging.error(f"⚠️ Fehler bei Ocean API (Standardwerte genutzt): {e}")

  # 2. Bitcoin & Ethereum (CoinGecko)
  btc_price, btc_change = 80921.0, 0.0
  eth_price, eth_change = 2510.0, 0.0

  try:
    cg_res = requests.get(
        CG_API_URL,
        params={
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        },
        timeout=10,
    ).json()

    btc_price = float(cg_res.get("bitcoin", {}).get("usd", btc_price))
    btc_change = float(cg_res.get("bitcoin", {}).get("usd_24h_change", 0.0))
    eth_price = float(cg_res.get("ethereum", {}).get("usd", eth_price))
    eth_change = float(cg_res.get("ethereum", {}).get("usd_24h_change", 0.0))
    logging.info("✅ CoinGecko API Daten erfolgreich erfasst.")
  except Exception as e:
    logging.error(f"⚠️ Fehler bei CoinGecko API: {e}")

  return dfi_data, btc_price, btc_change, eth_price, eth_change


# ==============================================================
# 2. MESSENGER DISPATCHERS (Telegram & Discord)
# ==============================================================
def send_telegram_update(text):
  """Versendet das Daily Update per Telegram Bot."""
  token = os.getenv("TELEGRAM_BOT_TOKEN")
  chat_id = os.getenv("TELEGRAM_CHAT_ID")

  if not token or not chat_id:
    logging.warning("⚠️ Telegram Credentials fehlen in Secrets. Übersprungen.")
    return

  url = f"https://api.telegram.org/bot{token}/sendMessage"
  payload = {
      "chat_id": chat_id,
      "text": text,
      "parse_mode": "Markdown",
      "disable_web_page_preview": True,
  }

  try:
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
      logging.info("✅ Telegram Nachricht gesendet.")
    else:
      logging.error(f"❌ Telegram Fehler {res.status_code}: {res.text}")
  except Exception as e:
    logging.error(f"❌ Telegram Ausnahme: {e}")


def send_discord_update(text):
  """Versendet das Daily Update an einen Discord Webhook."""
  webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

  if not webhook_url:
    logging.warning("⚠️ Discord Webhook URL fehlt in Secrets. Übersprungen.")
    return

  payload = {"content": text}

  try:
    res = requests.post(webhook_url, json=payload, timeout=10)
    if res.status_code in [200, 204]:
      logging.info("✅ Discord Nachricht gesendet.")
    else:
      logging.error(f"❌ Discord Fehler {res.status_code}: {res.text}")
  except Exception as e:
    logging.error(f"❌ Discord Ausnahme: {e}")


# ==============================================================
# 3. TEXT GENERATOR FOR MESSENGERS
# ==============================================================
def build_full_report(
    lang_code, dfi_data, btc_p, btc_c, eth_p, eth_c, insight_text, news_text
):
  """Erstellt den langen, ausführlichen Textbericht für Telegram & Discord."""
  dfi_sig = "🟢" if dfi_data["price_change_24h"] >= 0 else "🔴"
  btc_sig = "🟢" if btc_c >= 0 else "🔴"
  eth_sig = "🟢" if eth_c >= 0 else "🔴"

  report = f"""📊 *DeFiChain (DFI) Daily Update* ({lang_code.upper()})

*Markt-Übersicht:*
₿ BTC: ${btc_p:,.2f} ({btc_sig} {btc_c:.2f}%)
Ξ ETH: ${eth_p:,.2f} ({eth_sig} {eth_c:.2f}%)
💎 DFI: ${dfi_data['price_usd']:.6f} ({dfi_sig} {dfi_data['price_change_24h']:.2f}%)

*Supply & Tokenomics:*
🔥 Burned: {dfi_data['burned_dfi']/1e6:,.2f}M DFI
💧 Circulating: {dfi_data['circulating_supply']/1e6:,.2f}M DFI
📦 Total Supply: {dfi_data['total_supply']/1e6:,.2f}M DFI

💡 *Daily Insight:*
{insight_text}

📰 *Daily News:*
{news_text}

🌐 *DeFiScan:* https://defiscan.live
#DeFiChain #DFI #Crypto
"""
  return report


# ==============================================================
# 4. MAIN EXECUTION ROUTINE
# ==============================================================
def main():
  logging.info("🚀 Starte DeFiChain Multi-Platform Bot...")

  # 1. Daten abrufen
  dfi_data, btc_p, btc_c, eth_p, eth_c = fetch_market_data()

  # 2. Sprache definieren (aus Umgebungsvariable APP_LANG oder Fallback 'de')
  lang = os.getenv("APP_LANG", "de")
  logging.info(f"⚙️ Verarbeite Sprache: {lang}")

  # Dynamische Texte laden
  try:
    insight_text = get_daily_insight(lang)
  except Exception:
    insight_text = "Netzwerk-Parameter und Tokenomics verlaufen stabil."

  try:
    news_text = get_dfi_news(lang)
  except Exception:
    news_text = "Keine besonderen Ereignisse im Ökosystem."

  # A) Messenger-Report generieren und senden
  messenger_report = build_full_report(
      lang,
      dfi_data,
      btc_p,
      btc_c,
      eth_p,
      eth_c,
      insight_text,
      news_text,
  )

  send_telegram_update(messenger_report)
  send_discord_update(messenger_report)

  # B) X (Twitter) Thread versenden (mit strikter 280-Zeichen Kürzungs-Logik)
  try:
    logging.info("🐦 Starte X-Posting Routine...")
    post_x_thread_tweepy(
        dfi_data=dfi_data,
        btc_p=btc_p,
        btc_c=btc_c,
        eth_p=eth_p,
        eth_c=eth_c,
        lang_code=lang,
        insight_text=insight_text,
        news_text=news_text,
    )
  except Exception as e:
    logging.error(f"❌ Fehler bei der Ausführung von post_x_thread_tweepy: {e}")

  logging.info("🎉 Bot-Durchlauf erfolgreich abgeschlossen!")


if __name__ == "__main__":
  main()
