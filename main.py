# ==============================
# DeFiChain Daily Bot v3
# ==============================

from market import get_market_data
from network import get_network_data
from comparison import get_comparison
from news import get_dfi_news

from discord_bot import send_discord
from telegram_bot import send_telegram
from x_bot import send_x_thread


def main():
    print("🚀 DeFiChain Bot startet...")

    # ==========================
    # Daten holen
    # ==========================
    market = get_market_data()
    network = get_network_data()
    news = get_dfi_news()

    # Debug-Ausgabe zur Kontrolle der API-Struktur
    print("DEBUG network data:", network)

    # ==========================
    # Vergleich
    # ==========================
    comparison = get_comparison(market)

    # ==========================
    # Discord
    # ==========================
    send_discord(market, network, comparison, news)

    # ==========================
    # Market Daten
    # ==========================
    dfi = market.get("dfi", {})
    btc = market.get("bitcoin", {})
    eth = market.get("ethereum", {})

    # ==========================
    # Veränderungen
    # ==========================
    dfi_change = dfi.get("usd_24h_change", 0)
    btc_change = btc.get("usd_24h_change", 0)
    eth_change = eth.get("usd_24h_change", 0)

    dfi_signal = "🟢" if dfi_change >= 0 else "🔴"
    btc_signal = "🟢" if btc_change >= 0 else "🔴"
    eth_signal = "🟢" if eth_change >= 0 else "🔴"

    # ==========================
    # Burn Analyse & Tokenomics (Flexibel & Robust)
    # ==========================
    burned = network.get("burned_dfi") or network.get("burned") or network.get("burn") or {}

    if isinstance(burned, dict):
        total_burned = (
            burned.get("total")
            or burned.get("total_burned")
            or burned.get("amount")
            or network.get("total_burned")
            or 0
        )
        emission = (
            burned.get("emission")
            or burned.get("daily_emission")
            or network.get("daily_minted")
            or network.get("emission")
            or 0
        )
        address_burn = burned.get("address", 0)
        fee_burn = burned.get("fee", 0)
        auction_burn = burned.get("auction", 0)
        payback_burn = burned.get("payback", 0)
    else:
        total_burned = float(burned) if burned else 0
        emission = network.get("emission") or network.get("daily_minted") or 0
        address_burn = 0
        fee_burn = 0
        auction_burn = 0
        payback_burn = 0

    net_change = emission - total_burned

    if net_change > 0:
        token_status = f"🔴 Inflationär\n+{net_change:,.2f} DFI"
    else:
        token_status = f"🟢 Deflationär\n{net_change:,.2f} DFI"

    # Tokenomics-Dictionary für Ausgabebots aufbauen
    tokenomics_data = {
        "burned_dfi": total_burned if total_burned > 0 else "N/A",
        "daily_minted": emission if emission > 0 else "N/A"
    }

    # ==========================
    # DUSD Health & Intelligence
    # ==========================
    dusd = network.get("dusd", {})

    intelligence_data = {
        "total": dusd.get("health_score", 67),
        "status": dusd.get("status", "Stabil"),
        "daily_insight": f"🎯 {news.get('title', '')}\n\n{news.get('text', '')}"
    }

    # ==========================
    # Network Report
    # ==========================
    network_message = f"""
🌐 <b>Network & Tokenomics</b>

🪙 Existing DFI
{network.get('existing_dfi', 'N/A')}

━━━━━━━━━━━━━━

🔥 <b>DFI Burn</b>

🏠 Address Burn
{address_burn:,.2f} DFI

💸 Fee Burn
{fee_burn:,.2f} DFI

🔨 Auction Burn
{auction_burn:,.2f} DFI

↩️ Payback
{payback_burn:,.2f} DFI

🔥 Total Burned
{total_burned:,.2f} DFI

━━━━━━━━━━━━━━

📈 Emission
{emission:,.2f} DFI

⚖️ <b>Burn vs Emission</b>

{token_status}

━━━━━━━━━━━━━━

🪙 <b>DUSD Health Report</b>

💵 Price
${dusd.get('price', 'N/A')}

📉 Peg Deviation
{dusd.get('peg_difference', 'N/A')}

📊 Status
{dusd.get('status', 'N/A')}

❤️ Health Score
{dusd.get('health_score', 0)}/100

🔒 Locked DUSD
{dusd.get('locked', 'N/A')}

🔥 DUSD Burn
{dusd.get('burned', 'N/A')}

━━━━━━━━━━━━━━

⚖️ Excess DFI
{network.get('excess_dfi', 'N/A')}
"""

    # ==========================
    # Telegram Report
    # ==========================
    telegram_message = f"""
🚀 <b>DeFiChain Daily Update</b>

📅 {news.get('date', '')}

🤖 Report #{news.get('report', '')}

📚 History #{news.get('id', 0)}/100

━━━━━━━━━━━━━━

💰 <b>DFI Market</b>

💎 Price
🇺🇸 ${dfi.get('usd', 0):.8f}
🇪🇺 €{dfi.get('eur', 0):.8f}

📊 24h Change
{dfi_signal} {dfi_change:.2f}%

🏦 Market Cap
${dfi.get('usd_market_cap', 0):,.0f}

━━━━━━━━━━━━━━

🌍 <b>Crypto Market</b>

₿ Bitcoin
{btc_signal} {btc_change:.2f}%

Ξ Ethereum
{eth_signal} {eth_change:.2f}%

━━━━━━━━━━━━━━

{network_message}

━━━━━━━━━━━━━━

📰 <b>Daily Insight</b>

🎯 <b>{news.get('title', '')}</b>

{news.get('text', '')}

━━━━━━━━━━━━━━

#DeFiChain #DFI
"""

    send_telegram(telegram_message)

    # ==========================
    # X (Twitter) Thread
    # ==========================
    send_x_thread(
        insight=news.get('text', ''),
        tokenomics=tokenomics_data,
        dusd=dusd,
        network=network,
        intelligence=intelligence_data,
        global_crypto=market,
        market=market
    )

    print("✅ Bot fertig")


if __name__ == "__main__":
    main()
