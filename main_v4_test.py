# ======================================
# DeFiChain Intelligence v5
# Main Runner
# ======================================


from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.blockchain import get_blockchain_data

from modules.report_formatter import create_report
from modules.intelligence import calculate_intelligence_score
from insights import generate_daily_insight
from modules.history_engine import get_history


from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread


from language_manager import load_language




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


    load_language(language)



    # ==========================
    # Daten laden
    # ==========================


    market = get_market_data()

    tokenomics = get_tokenomics_data()

    dusd = get_dusd_data()

    community = get_community_data()

    blockchain = get_blockchain_data()



    # ==========================
    # Intelligence
    # ==========================


    intelligence = calculate_intelligence_score(

    market,

    tokenomics,

    dusd,

    community,

    blockchain

    )    


    print(
        f"🧠 Intelligence Score: {intelligence['total']} /100"
    )


    print(
        intelligence["status"]
    )



    # ==========================
    # Daily Insight
    # ==========================


    daily_insight = generate_daily_insight(

        market,

        tokenomics,

        dusd,

        blockchain

    )


    print(
        "💡 Daily Insight:"
    )

    print(
        daily_insight
    )



    # ==========================
    # History
    # ==========================


    history = get_history()


    if history:

        print(
            f"📚 History: {history['title']}"
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


        "burned_dfi":

            tokenomics.get(
                "burn",
                {}
            ).get(
                "total",
                "N/A"
            ),


        "locked_dusd":

            dusd.get(
                "locked",
                "N/A"
            ),


        "excess_dfi":

            tokenomics.get(
                "balance",
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
            "Daily DeFiChain Intelligence Report",


        "hashtags":
            "#DeFiChain #DFI"

    }



    # ==========================
    # Report
    # ==========================


    report = create_report(

        market,

        tokenomics,

        dusd,

        community,

        network,

        intelligence,

        daily_insight,

        history

    )



    # ==========================
    # Outputs
    # ==========================


    send_telegram(
        report
    )


    send_discord(

        market,

        network,

        comparison,

        news

    )


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
