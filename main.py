# ==============================
# DeFiChain Daily Bot v6 (Rotations-Lang & Total Supply)
# ==============================

from datetime import datetime
import os
import requests
from discord_bot import send_discord
from modules.language import load_language
from telegram_bot import send_telegram
from x_bot import format_large_number, send_x_thread

from comparison import get_comparison
from market import get_market_data
from news import get_dfi_news

# Sprachrotation für täglichen Wechsel
ROTATION_LANGUAGES = ["de", "en", "ru"]


def get_daily_language() -> str:
    """Berechnet die Tages-Sprache anhand des Tages im Jahr."""
    day_of_year = datetime.now().timetuple().tm_yday
    return ROTATION_LANGUAGES[day_of_year % len(ROTATION_LANGUAGES)]


def get_robust_dfi_data():
    """Holt DFI-Preis, Tokenomics und Supply-Metriken mit Fallbacks."""
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "price_usd": None,
        "price_change_24h": 0.0,
        "burned_dfi": 0.0,
        "daily_minted": 0.0,
        "total_supply": 0.0,
        "circulating_supply": 0.0,
    }

    try:
        stats_res = requests.get(
            "https://ocean.defichain.com/v0/mainnet/stats",
            headers=headers,
            timeout=4,
        ).json()
        stats_data = stats_res.get("data", {})
        supply_data = stats_data.get("tokens", {}).get("supply", {})

        data["burned_dfi"] = float(supply_data.get("burned", 0))
        data["total_supply"] = float(supply_data.get("total", 0))
        data["circulating_supply"] = float(supply_data.get("circulating", 0))
        data["daily_minted"] = float(
            stats_data.get("emission", {}).get("total", 0)
        )
    except Exception as e:
        print(f"⚠️ Ocean Stats API Fehler: {e}")

    try:
        price_res = requests.get(
            "https://ocean.defichain.com/v0/mainnet/prices/DFI-USD",
            headers=headers,
            timeout=4,
        ).json()
        data["price_usd"] = float(
            price_res.get("data", {})
            .get("price", {})
            .get("aggregated", {})
            .get("amount", 0)
        )
    except Exception as e:
        print(f"⚠️ Ocean Price API Fehler: {e}")

    # Fallbacks für leere Werte
    if data["burned_dfi"] <= 0:
        data["burned_dfi"] = 412500000.0
    if data["daily_minted"] <= 0:
        data["daily_minted"] = 288000.0
    if data["total_supply"] <= 0:
        data["total_supply"] = 1150000000.0
    if data["circulating_supply"] <= 0:
        data["circulating_supply"] = 829000000.0

    return data


def main():
    print("🚀 DeFiChain Bot startet...")

    # 1. Sprache per Rotation oder Environment wählen
    app_lang = os.getenv("APP_LANG", get_daily_language())
    print(f"🌐 Aktive Tages-Sprache: {app_lang.upper()}")
    lang = load_language(app_lang)

    # 2. Daten abrufen
    market = get_market_data()
    news = get_dfi_news()
    robust_dfi = get_robust_dfi_data()

    dfi_market = market.get("dfi", {})
    dfi_price = (
        robust_dfi["price_usd"]
        if robust_dfi["price_usd"]
        else dfi_market.get("usd", 0.003)
    )
    dfi_change = dfi_market.get(
        "usd_24h_change", robust_dfi["price_change_24h"]
    )

    btc = market.get("bitcoin", market.get("btc", {}))
    eth = market.get("ethereum", market.get("eth", {}))

    btc_price = float(btc.get("usd", btc.get("price", 0)))
    btc_change = float(btc.get("usd_24h_change", btc.get("change", 0)))

    eth_price = float(eth.get("usd", eth.get("price", 0)))
    eth_change = float(eth.get("usd_24h_change", eth.get("change", 0)))

    # 3. Datenstrukturen aufbauen
    x_market_data = {
        "btc_price": btc_price,
        "btc_change": btc_change,
        "eth_price": eth_price,
        "eth_change": eth_change,
        "dfi_price": dfi_price,
        "dfi_change": dfi_change,
    }

    tokenomics_data = {
        "burned_dfi": robust_dfi["burned_dfi"],
        "daily_minted": robust_dfi["daily_minted"],
        "total_supply": robust_dfi["total_supply"],
        "circulating_supply": robust_dfi["circulating_supply"],
    }

    intelligence_data = {
        "score": 67,
        "status": lang.get("status_stable", "Stabil"),
        "insight": f"🟢 Market recovery detected: DFI gained {dfi_change:.2f}% in 24h.",
    }

    network_data = {"network_status": "🟢 Online"}

    # 4. Telegram & Discord Ausgaben
    comparison = get_comparison(market)
    send_discord(market, network_data, comparison, news)

    dfi_signal = "🟢" if dfi_change >= 0 else "🔴"
    btc_signal = "🟢" if btc_change >= 0 else "🔴"
    eth_signal = "🟢" if eth_change >= 0 else "🔴"

    total_sup_str = format_large_number(robust_dfi["total_supply"])
    circ_sup_str = format_large_number(robust_dfi["circulating_supply"])
    burned_str = format_large_number(robust_dfi["burned_dfi"])
    minted_str = format_large_number(robust_dfi["daily_minted"])

    telegram_message = f"""
🚀 <b>{lang.get('header_title', 'DeFiChain Daily Update')}</b> ({app_lang.upper()})

📅 {news.get('date', '')}
🤖 Report #{news.get('report', '')}

━━━━━━━━━━━━━━

💰 <b>{lang.get('section_dfi', 'DFI Market & Tokenomics')}</b>
💎 {lang.get('label_price', 'Price')}: ${dfi_price:.6f} ({dfi_signal} {dfi_change:.2f}%)

📦 {lang.get('label_total_supply', 'Total Supply')}: {total_sup_str} DFI
💧 {lang.get('label_circulating', 'Circulating')}: {circ_sup_str} DFI
🔥 {lang.get('label_burned', 'Total Burned')}: {burned_str} DFI
🪙 {lang.get('label_minted', 'Daily Minted')}: {minted_str} DFI

━━━━━━━━━━━━━━

🌍 <b>{lang.get('section_crypto', 'Crypto Market')}</b>
₿ Bitcoin: ${btc_price:,.2f} ({btc_signal} {btc_change:.2f}%)
Ξ Ethereum: ${eth_price:,.2f} ({eth_signal} {eth_change:.2f}%)

━━━━━━━━━━━━━━

📰 <b>{lang.get('section_news', 'Daily Insight')}</b>
🎯 <b>{news.get('title', '')}</b>
{news.get('text', '')}

#DeFiChain #DFI
"""
    send_telegram(telegram_message)

    # 5. X Thread ausführen
    send_x_thread(
        insight=news.get("text", ""),
        tokenomics=tokenomics_data,
        dusd={},
        network=network_data,
        intelligence=intelligence_data,
        global_crypto=x_market_data,
        market=x_market_data,
        lang_code=app_lang.upper(),
    )

    print("✅ Bot erfolgreich ausgeführt.")


if __name__ == "__main__":
    main()
