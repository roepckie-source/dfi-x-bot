# ======================================
# DeFiChain Intelligence v5
# Main Test Runner
# ======================================

import sys
from pathlib import Path

# ======================================
# ROOT VERZEICHNIS
# ======================================

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ======================================
# MODULE
# ======================================

from modules.community import get_community_data
from modules.dusd import get_dusd_data
from modules.global_crypto import get_global_crypto
from modules.history_engine import get_history_chapter
from modules.insight_engine import generate_daily_insight
from modules.intelligence import calculate_intelligence_score
from modules.language import load_language
from modules.language_engine import get_next_language
from modules.market import get_market_data
from modules.network import get_network_data
from modules.tokenomics import get_tokenomics_data


# ======================================
# OUTPUTS
# ======================================

from outputs.discord_bot import send_discord
from outputs.telegram_bot import send_telegram
from outputs.x_bot import send_x_thread


# ======================================
# MAIN
# ======================================

def main():

    print(
        "🚀 DeFiChain Intelligence v5 startet..."
    )


    # ==================================
    # SPRACHE DES TAGES
    # ==================================

    language = get_next_language()

    print(
        f"🌍 Sprache: {language}"
    )

    load_language(language)


    # ==================================
    # MARKT
    # ==================================

    market = get_market_data()


    # ==================================
    # TOKENOMICS
    # ==================================

    tokenomics = get_tokenomics_data()


    # ==================================
    # dUSD
    # ==================================

    dusd = get_dusd_data()


    # ==================================
    # COMMUNITY
    # ==================================

    community = get_community_data()


    # ==================================
    # NETWORK
    # ==================================

    network = get_network_data()


    # ==================================
    # GLOBAL CRYPTO
    # ==================================

    global_crypto = get_global_crypto()

    print(
        "🌍 Global Crypto:"
    )

    print(
        global_crypto
    )


    # ==================================
    # INTELLIGENCE SCORE
    # ==================================

    intelligence = calculate_intelligence_score(
        market,
        tokenomics,
        dusd,
        community,
        network
    )


    score = intelligence.get(
        "total",
        0
    )


    # ==================================
    # STATUS
    # ==================================

    if score >= 80:

        status = "🟢 Sehr stark"

    elif score >= 60:

        status = "🟡 Stabil"

    elif score >= 40:

        status = "🟠 Vorsicht"

    else:

        status = "🔴 Kritisch"


    intelligence["status"] = status


    print(
        f"🧠 Intelligence Score: {score} /100"
    )

    print(
        status
    )


    # ==================================
    # HISTORY
    # ==================================

    try:

        current_history = get_history_chapter()

    except Exception as e:

        print(
            "⚠️ History Fehler:",
            e
        )

        current_history = None


    if current_history:

        print(
            "📚 History:",
            current_history.get(
                "title",
                "N/A"
            )
        )

    else:

        print(
            "📚 History: keine Daten"
        )


    # ==================================
    # DAILY INSIGHT
    # ==================================

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


    # ==================================
    # INTELLIGENCE DAILY INSIGHT
    # Für Kompatibilität mit x_bot
    # ==================================

    intelligence["daily_insight"] = daily_insight


    # ==================================
    # VERGLEICH BTC / ETH / DFI
    # ==================================

    try:

        dfi_change = float(
            market
            .get("dfi", {})
            .get("change", 0)
        )

    except Exception:

        dfi_change = 0


    try:

        btc_change = float(
            global_crypto
            .get("bitcoin", {})
            .get("change", 0)
        )

    except Exception:

        btc_change = 0


    try:

        eth_change = float(
            global_crypto
            .get("ethereum", {})
            .get("change", 0)
        )

    except Exception:

        eth_change = 0


    comparison = {

        "bitcoin": btc_change,

        "ethereum": eth_change,

        "dfi": dfi_change,

        "vs_btc": btc_change,

        "vs_eth": eth_change

    }


    # ==================================
    # REPORT
    # ==================================

    try:

        from modules.report_formatter import create_report

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

    except Exception as e:

        print(
            "⚠️ Report Fehler:",
            e
        )

        report = None


    # ==================================
    # TELEGRAM
    # ==================================

    try:

        if report:

            send_telegram(
                report
            )

    except Exception as e:

        print(
            "⚠️ Telegram Fehler:",
            e
        )


    # ==================================
    # DISCORD
    # ==================================

    try:

        send_discord(

            market,

            network,

            comparison,

            current_history

        )

    except Exception as e:

        print(
            "⚠️ Discord Fehler:",
            e
        )


    # ==================================
    # X THREAD
    # ==================================

    try:

        send_x_thread(

            market,

            tokenomics,

            dusd,

            network,

            intelligence,

            current_history,

            global_crypto,

            comparison,

            current_history,

            language

        )

    except Exception as e:

        print(
            "⚠️ X Fehler:",
            e
        )


    # ==================================
    # FERTIG
    # ==================================

    print(
        "✅ v5 Report gesendet"
    )


# ======================================
# START
# ======================================

if __name__ == "__main__":

    main()