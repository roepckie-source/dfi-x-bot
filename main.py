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
    # Telegram komplett
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


    telegram_message = f"""
🚀 <b>DeFiChain Daily Update</b>


📅 {news.get('date','')}

🤖 Report #{news.get('report','')}

📚 History #{news.get('id',0)}/100


━━━━━━━━━━━━━━


💰 <b>DFI Price</b>


🇺🇸 ${dfi.get('usd',0):.8f}

🇪🇺 €{dfi.get('eur',0):.8f}



📊 <b>24h Change</b>

{dfi.get('usd_24h_change',0):.2f}%



🏦 <b>Market Cap</b>

${dfi.get('usd_market_cap',0):,.0f}



━━━━━━━━━━━━━━


₿ <b>Bitcoin</b>

{btc.get('usd_24h_change',0):.2f}%



Ξ <b>Ethereum</b>

{eth.get('usd_24h_change',0):.2f}%



━━━━━━━━━━━━━━


🌐 <b>Network</b>

{network}



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
