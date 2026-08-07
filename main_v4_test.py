# ======================================
# DeFiChain Intelligence v5
# Main Runner
# ======================================


from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.blockchain import get_blockchain_data
from modules.global_crypto import get_global_crypto
from modules.language import load_language

from modules.report_formatter import create_report
from modules.intelligence import calculate_intelligence_score
from modules.insight_engine import generate_daily_insight
from modules.content_engine import get_content
from news import get_dfi_news


from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread


from modules.language_engine import get_next_language




def main():


    print(
        "🚀 DeFiChain Intelligence v5 startet..."
    )


    # ==========================
    # Sprache
    # ==========================


    language = get_next_language()


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

    global_crypto = get_global_crypto()

    print("🌍 Global Crypto:")
    print(global_crypto)

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

    score = intelligence.get("total", 0)

    if score >= 80:
        status = "🟢 Sehr stark"
    elif score >= 60:
        status = "🟡 Stabil"
    elif score >= 40:
        status = "🟠 Vorsicht"
    else:
        status = "🔴 Kritisch"

    intelligence["status"] = status

    print(f"🧠 Intelligence Score: {score} /100")
    print(status)


    # ==========================
    # History Engine v2
    # ==========================


    current_history = get_content()


    if current_history and isinstance(current_history, dict):

        print(
            f"📚 History: {current_history.get('title','N/A')}"
        )

    else:

        current_history = None

        print(
            "📚 History: keine Daten"
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
    # Daily Insight
    # ==========================


    daily_insight = generate_daily_insight(

        market,

        tokenomics,

        dusd,

        community,
        
        network,

        language

    )


    print(
        "💡 Daily Insight:"
    )

    print(
        daily_insight
    )


    # ==========================
    # Crypto Market Comparison
    # ==========================


    dfi_change = float(
        market.get("dfi", {}).get("change", 0)
    )


    btc_change = float(
        global_crypto.get("bitcoin", {}).get("change", 0)
    )


    eth_change = float(
        global_crypto.get("ethereum", {}).get("change", 0)
    )


    comparison = {

    "bitcoin":
        btc_change,

    "ethereum":
        eth_change,

    "dfi":
        dfi_change,

    # alte Discord-Kompatibilität
    "vs_btc":
        btc_change,

    "vs_eth":
        eth_change

    }

    # ==========================
    # Content / History
    # ==========================

    content = get_content()

    news = content

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
    current_history,
    global_crypto,
    comparison,
    language=language
)    



    # ==========================
    # Outputs
    # ==========================


    send_telegram(
        report,
        language
    )


    send_discord(

        market,

        network,

        comparison,

        news

    )


    send_x_thread(
    market,
    tokenomics,
    dusd,
    network,
    intelligence,
    current_history,
    global_crypto,
    comparison,
    news,
    language
    )
    



    print(
        "✅ v5 Report gesendet"
    )




if __name__ == "__main__":

    main()
