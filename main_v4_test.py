# ======================================
# DeFiChain Intelligence v4
# Main Test Runner
# ======================================


from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.blockchain import get_blockchain_data


from language_manager import load_language


from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread



def build_report(
        market,
        tokenomics,
        dusd,
        community,
        blockchain
):


    report = f"""
🚀 DeFiChain Daily Intelligence v4


💰 DFI Market

Price:
{market}


🔥 Tokenomics

Burn:
{tokenomics}


🪙 DUSD Health

{dusd}


🏦 Community Fund

{community}


⛓ Blockchain

{blockchain}

"""


    return report





def main():


    print(
        "🚀 DeFiChain Intelligence v4 startet..."
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
    # Adapter für alte Bots
    # ==========================


    network = {


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
            ),


        "excess_dfi":

            "N/A"

    }



    comparison = {


        "vs_btc":

            "N/A",


        "vs_eth":

            "N/A"

    }



    news = {


        "title":

            "DeFiChain Intelligence v4"


    }



    # ==========================
    # Report
    # ==========================


    report = build_report(

        market,

        tokenomics,

        dusd,

        community,

        blockchain

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
        "✅ v4 Report gesendet"
    )




if __name__ == "__main__":

    main()
