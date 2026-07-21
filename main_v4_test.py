# ==============================
# DeFiChain Daily Intelligence v4
# Main Controller
# ==============================


from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.blockchain import get_blockchain_data

from language_manager import (
    get_daily_language,
    load_language
)

from news import get_dfi_news

from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread



def main():


    print(
        "🚀 DeFiChain Intelligence v4 startet..."
    )



    # ==========================
    # Sprache bestimmen
    # ==========================

    language = get_daily_language()

    text = load_language(
        language
    )



    print(
        "🌍 Sprache:",
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


    news = get_dfi_news()



    # ==========================
    # Report erstellen
    # ==========================

    dfi = market.get(
        "dfi",
        {}
    )


    report = f"""

🚀 {text.get('title')}


🌐 Language

{language.upper()}


━━━━━━━━━━━━━━


💰 {text.get('market')}



💎 {text.get('price')}


🇺🇸 ${dfi.get('usd','N/A')}


🇪🇺 €{dfi.get('eur','N/A')}



📊 {text.get('change')}


{dfi.get('change','N/A')} %



🏦 {text.get('market_cap')}


${dfi.get('market_cap','N/A')}



━━━━━━━━━━━━━━


🔥 {text.get('tokenomics')}



🔥 {text.get('burn')}


{tokenomics.get('burn',{}).get('total')} DFI



📈 {text.get('emission')}


{tokenomics.get('emission')} DFI



⚖️ {text.get('net_burn')}


{tokenomics.get('net_change')}



{tokenomics.get('status')}



━━━━━━━━━━━━━━


🪙 {text.get('dusd')}



💵 Price


{dusd.get('price')}



❤️ Health


{dusd.get('health_score')}/100



━━━━━━━━━━━━━━


🏦 {text.get('community')}



DFI

{community.get('dfi')}



━━━━━━━━━━━━━━


⛓ {text.get('network')}



{blockchain.get('network_status')}


Block:

{blockchain.get('block_height')}



━━━━━━━━━━━━━━


📰 {text.get('insight')}


{news.get('title','')}


{news.get('text','')}



#DeFiChain #DFI

"""



    # ==========================
    # Ausgaben
    # ==========================

    send_telegram(
        report
    )

    comparison = {

    "vs_btc": "N/A",

    "vs_eth": "N/A"

    }

    network = {


    "existing_dfi":

        "N/A",



    "burned_dfi":

        tokenomics.get("burn", {}).get(
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

    print("DEBUG NETWORK:")
    print(network)


    send_discord(

    market,

    network,

    comparison,

    news

    )
    
    send_x_thread(
        report
    )
 

    print(
        "✅ v4 Report gesendet"
    )



if __name__ == "__main__":

    main()
