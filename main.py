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
    # Telegram Premium Report
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


    # DFI Signal

    dfi_change = dfi.get(
        "usd_24h_change",
        0
    )


    dfi_signal = (
        "🟢"
        if dfi_change >= 0
        else "🔴"
    )



    # BTC Signal

    btc_change = btc.get(
        "usd_24h_change",
        0
    )


    btc_signal = (
        "🟢"
        if btc_change >= 0
        else "🔴"
    )



    # ETH Signal

    eth_change = eth.get(
        "usd_24h_change",
        0
    )


    eth_signal = (
        "🟢"
        if eth_change >= 0
        else "🔴"
    )



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


🌐 <b>Network</b>



{network}



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
    # X Thread
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
