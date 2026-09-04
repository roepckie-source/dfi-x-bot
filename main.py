import os
import json
import logging
import requests
from datetime import datetime

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration & API Credentials
CONFIG = {
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "@your_channel_or_chat_id"),
    "DISCORD_WEBHOOK_URL": os.getenv("DISCORD_WEBHOOK_URL", "YOUR_DISCORD_WEBHOOK_URL"),
    "X_API_KEY": os.getenv("X_API_KEY", "YOUR_X_API_KEY"),
}

def fetch_crypto_metrics():
    """Holt aktuelle Marktdaten von öffentlichen APIs (z. B. CoinGecko)."""
    logging.info("Hole aktuelle Kryptomarktdaten...")
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=defichain,bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        return {
            "dfi_usd": data.get("defichain", {}).get("usd", 0.0018),
            "dfi_change": data.get("defichain", {}).get("usd_24h_change", 0.0),
            "btc_usd": data.get("bitcoin", {}).get("usd", 76800),
            "btc_change": data.get("bitcoin", {}).get("usd_24h_change", 0.0),
            "eth_usd": data.get("ethereum", {}).get("usd", 2380),
            "eth_change": data.get("ethereum", {}).get("usd_24h_change", 0.0),
            "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        }
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Marktdaten: {e}")
        # Fallback-Daten
        return {
            "dfi_usd": 0.0018, "dfi_change": 0.0,
            "btc_usd": 76800, "btc_change": 0.0,
            "eth_usd": 2380, "eth_change": 0.0,
            "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        }

def generate_tweets_and_posts(metrics):
    """Generiert alle vordefinierten Social-Media-Posts/Tweets in allen unterstützten Sprachen."""
    
    date_str = metrics["date"]
    dfi_p, dfi_c = metrics["dfi_usd"], metrics["dfi_change"]
    btc_p, btc_c = metrics["btc_usd"], metrics["btc_change"]
    eth_p, eth_c = metrics["eth_usd"], metrics["eth_change"]

    # 1. Deutsch (DE)
    post_de = (
        f"📊 **Krypto & DeFiChain Update ({date_str})**\n\n"
        f"🔹 **DFI:** ${dfi_p:.6f} ({dfi_c:+.2f}% 24h)\n"
        f"🔹 **BTC:** ${btc_p:,.2f} ({btc_c:+.2f}% 24h)\n"
        f"🔹 **ETH:** ${eth_p:,.2f} ({eth_c:+.2f}% 24h)\n\n"
        f"💡 Bleibt informiert & überprüft eure Handelsbots! #DeFiChain #DFI #Crypto #TradingBot #Bitcoin"
    )

    # 2. Englisch (EN - ru.json / en.json Struktur)
    post_en = (
        f"📊 **Crypto & DeFiChain Market Update ({date_str})**\n\n"
        f"🔹 **DFI:** ${dfi_p:.6f} ({dfi_c:+.2f}% 24h)\n"
        f"🔹 **BTC:** ${btc_p:,.2f} ({btc_c:+.2f}% 24h)\n"
        f"🔹 **ETH:** ${eth_p:,.2f} ({eth_c:+.2f}% 24h)\n\n"
        f"💡 Stay tuned & keep your automated strategies running! #DeFiChain #DFI #Crypto #Arbitrage #BTC"
    )

    # 3. Russisch (RU)
    post_ru = (
        f"📊 **Обновление рынка Crypto & DeFiChain ({date_str})**\n\n"
        f"🔹 **DFI:** ${dfi_p:.6f} ({dfi_c:+.2f}% за 24ч)\n"
        f"🔹 **BTC:** ${btc_p:,.2f} ({btc_c:+.2f}% за 24ч)\n"
        f"🔹 **ETH:** ${eth_p:,.2f} ({eth_c:+.2f}% за 24ч)\n\n"
        f"💡 Следите за обновлениями и проверяйте работу торговых ботов! #DeFiChain #DFI #Crypto #Bitcoin"
    )

    return {
        "DE": post_de,
        "EN": post_en,
        "RU": post_ru
    }

def send_to_telegram(message):
    """Sendet die Nachricht an den konfigurierten Telegram Channel/Bot."""
    bot_token = CONFIG["TELEGRAM_BOT_TOKEN"]
    chat_id = CONFIG["TELEGRAM_CHAT_ID"]
    
    if bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.warning("Telegram Bot Token nicht gesetzt. Überspringe Telegram-Versand.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            logging.info("Erfolgreich an Telegram gesendet!")
        else:
            logging.error(f"Telegram Fehler: {res.text}")
    except Exception as e:
        logging.error(f"Telegram Sende-Ausnahme: {e}")

def send_to_discord(message):
    """Sendet die Nachricht an den konfigurierten Discord Webhook."""
    webhook_url = CONFIG["DISCORD_WEBHOOK_URL"]
    
    if webhook_url == "YOUR_DISCORD_WEBHOOK_URL":
        logging.warning("Discord Webhook URL nicht gesetzt. Überspringe Discord-Versand.")
        return

    payload = {"content": message}
    try:
        res = requests.post(webhook_url, json=payload, timeout=10)
        if res.status_code in [200, 204]:
            logging.info("Erfolgreich an Discord gesendet!")
        else:
            logging.error(f"Discord Fehler: {res.text}")
    except Exception as e:
        logging.error(f"Discord Sende-Ausnahme: {e}")

def main():
    logging.info("Starte Live-Bot Update-Routine...")
    
    # 1. Metriken abrufen
    metrics = fetch_crypto_metrics()
    
    # 2. Posts & Tweets generieren
    posts = generate_tweets_and_posts(metrics)
    
    # 3. Ausgabe auf der Konsole (zum Testen/Review)
    print("\n" + "="*50)
    print("GENERIERTE TWEETS / POSTS:")
    print("="*50)
    for lang, text in posts.items():
        print(f"\n--- [{lang}] ---")
        print(text)
    print("="*50 + "\n")

    # 4. Automatisierter Versand (Hauptnachricht auf Englisch / Deutsch)
    send_to_telegram(posts["EN"])
    send_to_discord(posts["EN"])

if __name__ == "__main__":
    main()
