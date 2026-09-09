# ==============================================================
# DeFiChain Intelligence v5
# MAIN RUNNER
#
# Einziger Einstiegspunkt des Bots
# Telegram + Discord + X
# ==============================================================
 
import sys
import logging
from pathlib import Path


# ==============================================================
# ROOT PATH
# ==============================================================

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ==============================================================
# MODULES
# ==============================================================

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

from news import get_dfi_news

from modules.report_formatter import create_report

from outputs.telegram_bot import send_telegram_report
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread


# ==============================================================
# LOGGING
# ==============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================================================
# HELPER
# ==============================================================

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ==============================================================
# MAIN
# ==============================================================

def main():

    logging.info("==================================================")
    logging.info("🚀 DeFiChain Intelligence v5")
    logging.info("==================================================")

    # ----------------------------------------------------------
    # 1. SPRACHE DES TAGES
    # ----------------------------------------------------------

    try:
        language = get_next_language()
        load_language(language)

        logging.info(
            f"🌍 Sprache des Tages: {language.upper()}"
        )

    except Exception as e:

        logging.error(
            f"❌ Sprachmodul Fehler: {e}"
        )

        language = "de"

        try:
            load_language(language)
        except Exception:
            pass


    # ----------------------------------------------------------
    # 2. MARKET
    # ----------------------------------------------------------

    try:

        market = get_market_data()

        logging.info("📊 Market Daten geladen")

    except Exception as e:

        logging.error(
            f"❌ Market Fehler: {e}"
        )

        market = {
            "price": 0.0,
            "change_24h": 0.0,
            "market_cap": 0.0,
            "volume": 0.0,
            "dfi": {
                "usd": 0.0,
                "change": 0.0
            }
        }


    # ----------------------------------------------------------
    # 3. GLOBAL CRYPTO
    # ----------------------------------------------------------

    try:

        global_crypto = get_global_crypto()

        logging.info("🌍 BTC / ETH Daten geladen")

        btc = global_crypto.get(
            "bitcoin",
            {}
        )

        eth = global_crypto.get(
            "ethereum",
            {}
        )

        logging.info(
            f"₿ BTC: ${btc.get('price', 'N/A')} "
            f"({btc.get('change', 'N/A')}%)"
        )

        logging.info(
            f"Ξ ETH: ${eth.get('price', 'N/A')} "
            f"({eth.get('change', 'N/A')}%)"
        )

    except Exception as e:

        logging.error(
            f"❌ Global Crypto Fehler: {e}"
        )

        global_crypto = {
            "bitcoin": {
                "price": "N/A",
                "change": "N/A"
            },
            "ethereum": {
                "price": "N/A",
                "change": "N/A"
            }
        }


    # ----------------------------------------------------------
    # 4. TOKENOMICS
    # ----------------------------------------------------------

    try:

        tokenomics = get_tokenomics_data()

        burn = tokenomics.get(
            "burn",
            {}
        )

        total_burn = burn.get(
            "total",
            0
        )

        emission = tokenomics.get(
            "emission",
            0
        )

        net_change = tokenomics.get(
            "net_change",
            0
        )

        logging.info(
            f"🔥 Burn: {total_burn:,.2f} DFI"
        )

        logging.info(
            f"🪙 Emission: {emission:,.2f} DFI"
        )

        logging.info(
            f"📈 Net Change: {net_change:,.2f} DFI"
        )

        logging.info(
            f"📊 Tokenomics: "
            f"{tokenomics.get('status', 'N/A')}"
        )

    except Exception as e:

        logging.error(
            f"❌ Tokenomics Fehler: {e}"
        )

        tokenomics = {}


    # ----------------------------------------------------------
    # 5. dUSD
    # ----------------------------------------------------------

    try:

        dusd = get_dusd_data()

        logging.info(
            f"💵 dUSD: "
            f"${dusd.get('price', 'N/A')}"
        )

        logging.info(
            f"🩺 dUSD Health: "
            f"{dusd.get('health_score', 'N/A')}"
        )

    except Exception as e:

        logging.error(
            f"❌ dUSD Fehler: {e}"
        )

        dusd = {}


    # ----------------------------------------------------------
    # 6. COMMUNITY
    # ----------------------------------------------------------

    try:

        community = get_community_data()

        logging.info(
            "👥 Community Daten geladen"
        )

    except Exception as e:

        logging.error(
            f"⚠️ Community Fehler: {e}"
        )

        community = {}


    # ----------------------------------------------------------
    # 7. NETWORK
    # ----------------------------------------------------------

    try:

        network = get_network_data()

        logging.info(
            "⛓ Network Daten geladen"
        )

    except Exception as e:

        logging.error(
            f"⚠️ Network Fehler: {e}"
        )

        network = {}


    # ----------------------------------------------------------
    # 8. INTELLIGENCE SCORE
    # ----------------------------------------------------------

    try:

        intelligence = calculate_intelligence_score(
            market,
            tokenomics,
            dusd,
            community,
            network
        )

        if not isinstance(
            intelligence,
            dict
        ):
            intelligence = {}

        score = safe_float(
            intelligence.get(
                "total",
                0
            )
        )

        if score >= 80:

            status = "🟢 Sehr stark"

        elif score >= 60:

            status = "🟡 Stabil"

        elif score >= 40:

            status = "🟠 Vorsicht"

        else:

            status = "🔴 Kritisch"

        intelligence["status"] = status

        logging.info(
            f"🧠 Intelligence Score: "
            f"{score:.0f}/100"
        )

        logging.info(
            f"📊 Status: {status}"
        )

    except Exception as e:

        logging.error(
            f"❌ Intelligence Fehler: {e}"
        )

        intelligence = {
            "total": 0,
            "status": "🔴 Kritisch"
        }


    # ----------------------------------------------------------
    # 9. HISTORY
    # ----------------------------------------------------------

    try:

        current_history = get_history_chapter()

        if current_history:

            logging.info(
                "📚 History: "
                + str(
                    current_history.get(
                        "title",
                        "N/A"
                    )
                )
            )

        else:

            logging.info(
                "📚 History: keine Daten"
            )

    except Exception as e:

        logging.error(
            f"⚠️ History Fehler: {e}"
        )

        current_history = None


    # ----------------------------------------------------------
    # 10. NEWS
    # ----------------------------------------------------------

    try:

        # Normaler Aufruf
        news = get_dfi_news()

        if isinstance(news, dict):

            logging.info(
                "📰 News: "
                + str(
                    news.get(
                        "title",
                        "N/A"
                    )
                )
            )

        else:

            logging.info(
                f"📰 News: {news}"
            )

    except TypeError:

        # Kompatibilität mit älterer News-Funktion
        try:

            news = get_dfi_news(
                lang=language,
                advance_day=True
            )

            logging.info(
                "📰 News geladen"
            )

        except Exception as e:

            logging.error(
                f"⚠️ News Fehler: {e}"
            )

            news = None

    except Exception as e:

        logging.error(
            f"⚠️ News Fehler: {e}"
        )

        news = None


    # ----------------------------------------------------------
    # 11. DAILY INSIGHT
    # ----------------------------------------------------------

    try:

        daily_insight = generate_daily_insight(
            language
        )

        if not daily_insight:
            daily_insight = ""

        logging.info(
            "💡 Daily Insight erzeugt"
        )

    except Exception as e:

        logging.error(
            f"⚠️ Daily Insight Fehler: {e}"
        )

        daily_insight = ""


    intelligence["daily_insight"] = daily_insight


    # ----------------------------------------------------------
    # 12. REPORT
    # ----------------------------------------------------------

    try:

        dfi = market.get(
            "dfi",
            {}
        )

        btc = global_crypto.get(
            "bitcoin",
            {}
        )

        eth = global_crypto.get(
            "ethereum",
            {}
        )

        comparison = {

            "dfi": {
                "price": dfi.get(
                    "usd",
                    0
                ),
                "change": dfi.get(
                    "change",
                    0
                )
            },

            "bitcoin": {
                "price": btc.get(
                    "price",
                    0
                ),
                "change": btc.get(
                    "change",
                    0
                )
            },

            "ethereum": {
                "price": eth.get(
                    "price",
                    0
                ),
                "change": eth.get(
                    "change",
                    0
                )
            }
        }

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
            news=news,
            language=language
        )

        logging.info(
            "📄 Report erfolgreich erstellt"
        )

    except Exception as e:

        logging.error(
            f"❌ Report Fehler: {e}"
        )

        report = None

        comparison = {
            "dfi": {
                "price": 0,
                "change": 0
            }
        }


    # ==========================================================
    # 13. TELEGRAM
    # ==========================================================

    try:

        telegram_ok = send_telegram_report(

            report or daily_insight,
            tokenomics,
            dusd,
            network,
            intelligence,
            current_history,
            global_crypto,
            market
        )

        if telegram_ok:

            logging.info(
                "📨 Telegram erfolgreich gesendet"
            )

        else:

            logging.warning(
                "⚠️ Telegram wurde nicht gesendet"
            )

    except Exception as e:

        logging.error(
            f"❌ Telegram Fehler: {e}"
        )


    # ==========================================================
    # 14. DISCORD
    # ==========================================================

    try:

        discord_ok = send_discord(

            daily_insight,
            network,
            comparison,
            news
        )

        if discord_ok:

            logging.info(
                "💬 Discord erfolgreich gesendet"
            )

        else:

            logging.warning(
                "⚠️ Discord wurde nicht gesendet"
            )

    except Exception as e:

        logging.error(
            f"❌ Discord Fehler: {e}"
        )


    # ==========================================================
    # 15. X
    # ==========================================================

    try:

        x_ok = send_x_thread(

            report,
            tokenomics,
            dusd,
            network,
            intelligence,
            current_history,
            global_crypto,
            market
        )

        if x_ok:

            logging.info(
                "🐦 X Thread erfolgreich gesendet"
            )

        else:

            logging.warning(
                "⚠️ X Thread wurde nicht gesendet"
            )

    except Exception as e:

        logging.error(
            f"❌ X Fehler: {e}"
        )


    # ==========================================================
    # FERTIG
    # ==========================================================

    logging.info("==================================================")
    logging.info("🎉 DeFiChain Daily Bot abgeschlossen")
    logging.info("==================================================")


# ==============================================================
# START
# ==============================================================

if __name__ == "__main__":
    main()
