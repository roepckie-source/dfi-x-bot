# ==============================
# DeFiChain Daily Bot v2
# ==============================


from market import get_market_data
from network import get_network_data
from comparison import get_comparison
from news import get_dfi_news

from discord_bot import send_discord
from telegram_bot import send_telegram
from x_bot import send_x_thread



def main():

    print(
        "🚀 DeFiChain Bot startet..."
    )


    # ==========================
    # Daten holen
    # ==========================

    market = get_market_data()

    network = get_network_data()

    news = get_dfi_news()



    # ==========================
    # Vergleich
    # ==========================

    comparison = get_comparison(
        market
    )



    # ==========================
    # Discord
    # ==========================

    send_discord(
        market,
        network,
        comparison,
        news
    )



    # ==========================
    # Telegram Daten vorbereiten
    # ==========================

    dfi = market.get(
        "dfi",
        {}
    )

    btc = market.get(
        "bitcoin",
        {}
    )

    eth = market.get(
        "ethereum",
        {}
    )


    burned = network.get(
        "burned_dfi",
        {}
    )



    # ==========================
    # Signale
    # ==========================

    dfi_change = dfi.get(
        "usd_24h_change",
        0
    )

    btc_change = btc.get(
        "usd_24h_change",
        0
    )

    eth_change = eth.get(
        "usd_24h_change",
        0
    )


    dfi_signal = (
        "🟢"
        if dfi_change >= 0
        else "🔴"
    )

    btc_signal = (
        "🟢"
        if btc_change >= 0
        else "🔴"
    )

    eth_signal = (
        "🟢"
        if eth_change >= 0
        else "🔴"
    )



    # ==========================
    # Network Format
    # ==========================

    network_message = f"""
🌐 <b>Network & Tokenomics</b>


🪙 <b>Existing DFI</b>

{network.get('existing_dfi','N/A')}



━━━━━━━━━━━━━━


🔥 <b>Burned DFI</b>


🏠 Address Burn

{burned.get('address',0):,.2f} DFI


💸 Fee Burn

{burned.get('fee',0):,.2f} DFI


🔨 Auction Burn

{burned.get('auction',0):,.2f} DFI


↩️ Payback

{burned.get('payback',0):,.2f} DFI


📈 Emission

{burned.get('emission',0):,.2f} DFI


🔥 <b>Total Burned</b>

{burned.get('total',0):,.2f} DFI



━━━━━━━━━━━━━━


🔒 <b>Locked DUSD</b>

{network.get('locked_dusd','N/A')}



⚖️ <b>Excess DFI</b>

{network.get('excess_dfi','N/A')}
"""



    # ==========================
    # Telegram Nachricht
    # ==========================

    telegram_message = f"""
🚀 <b>DeFiChain Daily Update</b>


📅 {news.get('date','')}

🤖 Report #{news.get('report','')}

📚 History #{news.get('id',0)}/100



━━━━━━━━━━━━━━


💰 <b>DFI Market</b>


💎 Price

🇺🇸 ${dfi.get('usd',0):.8f}

🇪🇺 €{dfi.get('eur',0):.8f}


📊 24h Change

{dfi_signal} {dfi_change:.2f}%


🏦 Market Cap

${dfi.get('usd_market_cap',0):,.0f}



━━━━━━━━━━━━━━


🌍 <b>Crypto Market</b>


₿ Bitcoin

{btc_signal} {btc_change:.2f}%


Ξ Ethereum

{eth_signal} {eth_change:.2f}



━━━━━━━━━━━━━━


{network_message}



━━━━━━━━━━━━━━


📰 <b>Daily Insight</b>


🎯 <b>{news.get('title','')}</b>


{news.get('text','')}



━━━━━━━━━━━━━━


🪙 <b>DUSD Status</b>

Coming soon...



━━━━━━━━━━━━━━


#DeFiChain #DFI
"""



    send_telegram(
        telegram_message
    )



    # ==========================
    # X
    # ==========================

    send_x_thread(
        market,
        network,
        comparison,
        news
    )



    print(
        "✅ Bot fertig"
    )



if __name__ == "__main__":

    main()
