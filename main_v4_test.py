# ======================================
# DeFiChain Intelligence v5
# Main Test Runner
# + Daily Insight Engine
# ======================================


from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.blockchain import get_blockchain_data

from modules.report_formatter import create_report

from modules.intelligence import (
    calculate_intelligence_score,
    get_score_status
)

from modules.insight_engine import (
    generate_daily_insight
)

from language_manager import load_language


from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread





def main():


    print(
        "🚀 DeFiChain Intelligence v5 startet..."
    )



    # ==========================
    # Sprache
    # ==========================

    language = "de"


    print(
        f"🌍 Sprache: {language}"
    )


    load_language(
        language
    )



    # ==========================
    # Daten laden
    # ==========================


    market = get_market_data()


    tokenomics = get_tokenomics_data()


    dusd = get_dusd_data()


    community = get_community_data()


    blockchain = get_blockchain_data()



    # ==========================
    # Intelligence Score
    # ==========================


    intelligence = calculate_intelligence_score(

        market,

        tokenomics,

        dusd,

        community,

        blockchain

    )


    print(
        "🧠 Intelligence Score:",
        intelligence["total"],
        "/100"
    )


    print(
        get_score_status(
            intelligence["total"]
        )
    )



    # ==========================
    # Daily Insight
    # ==========================


    daily_insight = generate_daily_insight(

        market,

        tokenomics,

        dusd,

        community,

        blockchain

    )


    print(
        "💡 Daily Insight:"
    )


    print(
        daily_insight
    )



    # ==========================
    # Network Adapter
    # ==========================


    network = {


        "network_status":

            blockchain.get(
                "network_status",
                "🟢 Online"
            ),



        "block_height":

            blockchain.get(
                "block_height",
                "N/A"
            ),



        "last_block_time":

            blockchain.get(
                "last_block_time",
                "N/A"
            ),



        "masternodes":

            blockchain.get(
                "masternodes",
                "N/A"
            ),



        "existing_dfi":

            "N/A",



        "burned_dfi":

            tokenomics
            .get(
                "burn",
                {}
            )
            .get(
                "total",
                "N/A"
            ),



        "locked_dusd":

            dusd.get(
                "locked_dusd",
                "N/A"
            )

    }




    # ==========================
    # Vergleich
    # ==========================


    comparison = {


        "vs_btc":

            "N/A",


        "vs_eth":

            "N/A"

    }




    # ==========================
    # News
    # ==========================


    news = {


        "title":

            "DeFiChain Intelligence v5",



        "text":

            daily_insight,



        "hashtags":

            "#DeFiChain #DFI"

    }




    # ==========================
    # Report erstellen
    # ==========================


    report = create_report(

        market,

        tokenomics,

        dusd,

        community,

        network,

        intelligence,

        daily_insight

    )



    # ==========================
    # Telegram
    # ==========================


    send_telegram(

        report

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
    # X
    # ==========================


    send_x_thread(

        market,

        network,

        comparison,

        news

    )



    print(
        "✅ v5 Report gesendet"
    )





if __name__ == "__main__":

    main()
