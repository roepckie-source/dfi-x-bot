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
    # Market Daten
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



    # ==========================
    # Veränderungen
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
    # Burn Analyse
    # ==========================

    burned = network.get(
        "burned_dfi",
        {}
    )


    total_burned = burned.get(
        "total",
        0
    )


    emission = burned.get(
        "emission",
        0
    )


    net_change = emission - total_burned



    if net_change > 0:

        token_status = (
            "🔴 Inflationär\n"
            f"+{net_change:,.2f} DFI"
        )

    else:

        token_status = (
            "🟢 Deflationär\n"
            f"{net_change:,.2f} DFI"
        )



    # ==========================
    # DUSD Health
    # ==========================

    dusd = network.get(
        "dusd",
        {}
    )



    # ==========================
    # Network Report
    # ==========================

    network_message = f"""
🌐 <b>Network & Tokenomics</b>


🪙 Existing DFI

{network.get('existing_dfi','N/A')}



━━━━━━━━━━━━━━


🔥 <b>DFI Burn</b>


🏠 Address Burn

{burned.get('address',0):,.2f} DFI


💸 Fee Burn

{burned.get('fee',0):,.2f} DFI


🔨 Auction Burn

{burned.get('auction',0):,.2f} DFI


↩️ Payback

{burned.get('payback',0):,.2f} DFI


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

${dusd.get('price','N/A')}



📉 Peg Deviation

{dusd.get('peg_difference','N/A')}



📊 Status

{dusd.get('status','N/A')}



❤️ Health Score

{dusd.get('health_score',0)}/100



🔒 Locked DUSD

{dusd.get('locked','N/A')}



🔥 DUSD Burn

{dusd.get('burned','N/A')}



━━━━━━━━━━━━━━


⚖️ Excess DFI

{network.get('excess_dfi','N/A')}
"""



    # ==========================
    # Telegram Report
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

{eth_signal} {eth_change:.2f}%



━━━━━━━━━━━━━━


{network_message}



━━━━━━━━━━━━━━


📰 <b>Daily Insight</b>



🎯 <b>{news.get('title','')}</b>



{news.get('text','')}



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
