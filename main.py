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
