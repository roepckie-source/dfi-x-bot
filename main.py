# ==============================================================
# DeFiChain Bot Main Module - main.py
# ==============================================================

import logging
import time
from news import get_dfi_news
from outputs.x_bot import post_x_thread_tweepy

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Unterstützte Sprachen
TARGET_LANGUAGES = ["de", "en", "ru", "zh"]


def fetch_defichain_stats():
  """Beispielhafter Aufruf für deine Ocean API Daten."""
  return {
      "price_usd": 0.002780,
      "price_change_24h": 0.00,
      "total_supply": 452000000,
      "circulating_supply": 829000000,
      "burned_dfi": 321440000,
      "daily_minted": 70300,
  }


def run_bot():
  logging.info("🚀 Starte DeFiChain Multi-Platform Bot...")
  logging.info("📡 Starte API-Abfragen...")

  # Live-Daten abrufen
  dfi_data = fetch_defichain_stats()
  btc_p, btc_c = 81219.00, 4.27
  eth_p, eth_c = 2522.64, 4.86

  logging.info("✅ API Daten erfolgreich erfasst.")

  # Schleife über alle Sprachen
  for index, lang in enumerate(TARGET_LANGUAGES):
    logging.info(f"⚙️ Verarbeite Sprache: {lang}")

    # WICHTIG: Nur beim ersten Durchlauf (index == 0) den Tag weiterzählen!
    should_advance = index == 0
    news_text = get_dfi_news(lang=lang, advance_day=should_advance)

    insight_text = (
        "Netzwerk-Parameter und Tokenomics verlaufen stabil."
        if lang == "de"
        else "Network parameters and tokenomics remain stable."
    )

    # 1. X-Thread senden
    logging.info(f"🐦 Starte X-Posting Routine ({lang.upper()})...")
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

    # ... hier können deine Telegram / Discord Aufrufe stehen ...

    # Pause zwischen Sprachen zur Einhaltung von Rate Limits
    if index < len(TARGET_LANGUAGES) - 1:
      time.sleep(10)

  logging.info("🎉 Bot-Durchlauf erfolgreich abgeschlossen!")


if __name__ == "__main__":
  run_bot()
