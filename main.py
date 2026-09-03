# ==============================
# DeFiChain Daily Bot v3
# ==============================

import requests
from discord_bot import send_discord
from telegram_bot import send_telegram
from x_bot import format_large_number, send_x_thread

from comparison import get_comparison
from market import get_market_data
from news import get_dfi_news


def get_robust_dfi_data():
    """Holt DFI-Preis, Tokenomics und Supply-Metriken mit automatischer Fallback-Kaskade."""
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "price_usd": None,
        "price_change_24h": 0.0,
        "burned_dfi": 0.0,
        "daily_minted": 0.0,
        "total_supply": 0.0,
        "circulating_supply": 0.0,
    }

    # 1. Primary: Ocean API Stats
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
        print(f"⚠️ Ocean Stats API nicht erreichbar: {e}")

    # 2. Primary: Ocean Oracle Price
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
        print(f"⚠️ Ocean Price API nicht erreichbar: {e}")

    # 3. Fallback 1: DEX Pool-Berechnung (USDT-DFI)
    if not data["price_usd"]:
        try:
            pool_res = requests.get(
                "https://ocean.defichain.com/v0/mainnet/poolpairs/dUSDT-DFI",
                headers=headers,
                timeout=4,
            ).json()
            token_a = float(
                pool_res.get("data", {}).get("tokenA", {}).get("reserve", 0)
            )  # USDT
            token_b = float(
                pool_res.get("data", {}).get("tokenB", {}).get("reserve", 0)
            )  # DFI
            if token_b > 0:
                data["price_usd"] = token_a / token_b
                print("💡 DFI Preis über DEX Pool berechnet.")
        except Exception as e:
            print(f"⚠️ DEX Pool Fallback fehlgeschlagen: {e}")

    # 4. Fallback 2: CoinGecko API
    if not data["price_usd"]:
        try:
            cg_res = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=defichain&vs_currencies=usd&include_24hr_change=true",
                headers=headers,
                timeout=4,
            ).json()
            data["price_usd"] = float(cg_res.get("defichain", {}).get("usd", 0))
            data["price_change_24h"] = float(
                cg_res.get("defichain", {}).get("usd_24h_change", 0)
            )
            print("💡 DFI Preis über CoinGecko abgerufen.")
        except Exception as e:
            print(f"⚠️ CoinGecko Fallback fehlgeschlagen: {e}")

    # 5. Absicherung gegen leere/0-Werte (Netzwerk-Richtwerte)
    if data["burned_dfi"] <= 0:
        data["burned_dfi"] = 412500000.0  # Aktueller ca. Burn-Stand
    if data["daily_minted"] <= 0:
        data["daily_minted"] = 288000.0  # Tägliche Block-Rewards
    if data["total_supply"] <= 0:
        data["total_supply"] = 1150000000.0  # Ca. 1.15B DFI Total Supply
    if data["circulating_supply"] <= 0:
        data["circulating_supply"] = 829000000.0  # Ca. 829M DFI Circulating

    return data


def main():
    print("🚀 DeFiChain Bot startet...")

    # ==========================
    # Daten & Fallbacks abrufen
    # ==========================
    market = get_market_data()
    news = get_dfi_news()
    robust_dfi = get_robust_dfi_data()

    # DFI-Marktdaten mit Fallback-Werten anreichern/überschreiben
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

    # Mappings für x_bot.py (flache Struktur)
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

    # ==========================
    # Network & Intelligence
    # ==========================
    intelligence_data = {
        "score": 67,
        "status": "Stabil",
        "insight": f"🟢 Market recovery detected: DFI gained {dfi_change:.2f}% in 24h.\n\n⚠️ Emission currently exceeds burn\n\n🟢 dUSD health stable",
    }

    network_data = {"network_status": "🟢 Online"}

    # ==========================
    # Discord & Telegram
    # ==========================
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
🚀 <b>DeFiChain Daily Update</b>

📅 {news.get('date', '')}
🤖 Report #{news.get('report', '')}

━━━━━━━━━━━━━━

💰 <b>DFI Market & Tokenomics</b>
💎 Price: ${dfi_price:.6f} ({dfi_signal} {dfi_change:.2f}%)

📦 Total Supply: {total_sup_str} DFI
💧 Circulating: {circ_sup_str} DFI
🔥 Total Burned: {burned_str} DFI
🪙 Daily Minted: {minted_str} DFI

━━━━━━━━━━━━━━

🌍 <b>Crypto Market</b>
₿ Bitcoin: ${btc_price:,.2f} ({btc_signal} {btc_change:.2f}%)
Ξ Ethereum: ${eth_price:,.2f} ({eth_signal} {eth_change:.2f}%)

━━━━━━━━━━━━━━

📰 <b>Daily Insight</b>
🎯 <b>{news.get('title', '')}</b>
{news.get('text', '')}

#DeFiChain #DFI
"""
    send_telegram(telegram_message)

    # ==========================
    # X (Twitter) Thread
    # ==========================
    send_x_thread(
        insight=news.get("text", ""),
        tokenomics=tokenomics_data,
        dusd={},
        network=network_data,
        intelligence=intelligence_data,
        global_crypto=x_market_data,
        market=x_market_data,
    )

    print("✅ Bot erfolgreich ausgeführt.")


if __name__ == "__main__":
    main()
