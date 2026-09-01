# ======================================
# DeFiChain Intelligence v5
# Main Test Runner
# ======================================

import sys
import traceback
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

from news import get_dfi_news
from charts import generate_all_charts


# ======================================
# OUTPUTS
# ======================================

from outputs.discord_bot import send_discord
from outputs.telegram_bot import send_telegram
from outputs.x_bot import send_x_thread


# ======================================
# MAIN LOGIK
# ======================================

def main():
    print("🚀 DeFiChain Intelligence v5 startet...", flush=True)

    # 1. Sprache
    language = get_next_language()
    print(f"🌍 Sprache: {language}", flush=True)
    load_language(language)

    # 2. Daten abrufen
    market = get_market_data()
    tokenomics = get_tokenomics_data()
    dusd = get_dusd_data()
    community = get_community_data()
    network = get_network_data()
    global_crypto = get_global_crypto()

    # 3. Intelligence Score
    intelligence = calculate_intelligence_score(
        market, tokenomics, dusd, community, network
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
    print(f"🧠 Intelligence Score: {score} /100 -> {status}", flush=True)

    # 4. History & News
    try:
        current_history = get_history_chapter()
    except Exception as e:
        print(f"⚠️ History Fehler: {e}", flush=True)
        current_history = None

    try:
        news = get_dfi_news()
    except Exception as e:
        print(f"⚠️ News Fehler: {e}", flush=True)
        news = None

    # 5. Daily Insight
    try:
        daily_insight = generate_daily_insight(language)
    except Exception as e:
        print(f"⚠️ Daily Insight Fehler: {e}", flush=True)
        daily_insight = ""

    intelligence["daily_insight"] = daily_insight

    # 6. Vergleich
    try:
        dfi_change = float(market.get("dfi", {}).get("change", 0))
    except Exception:
        dfi_change = 0

    try:
        btc_change = float(global_crypto.get("bitcoin", {}).get("change", 0))
    except Exception:
        btc_change = 0

    try:
        eth_change = float(global_crypto.get("ethereum", {}).get("change", 0))
    except Exception:
        eth_change = 0

    comparison = {
        "bitcoin": btc_change,
        "ethereum": eth_change,
        "dfi": dfi_change,
        "vs_btc": btc_change,
        "vs_eth": eth_change
    }

    # 7. Charts & GIF generieren
    try:
        print("📊 Generiere Charts für Bot-Outputs...", flush=True)
        generate_all_charts(
            market=market,
            tokenomics=tokenomics,
            dusd=dusd,
            intelligence=intelligence,
            global_crypto=global_crypto
        )
        print("✅ Charts erfolgreich im Ordner outputs/ erstellt.", flush=True)
    except Exception as e:
        print(f"⚠️ Fehler beim Generieren der Charts: {e}", flush=True)

    # 8. Report Formatter
    try:
        from modules.report_formatter import create_report
        report = create_report(
            market, tokenomics, dusd, community, network,
            intelligence, daily_insight, current_history,
            global_crypto, comparison, news=news, language=language
        )
    except Exception as e:
        print(f"⚠️ Report Fehler: {e}", flush=True)
        report = None

    # 9. Outputs versenden
    # Telegram
    try:
        if report:
            send_telegram(report)
            print("📨 Telegram erfolgreich gesendet", flush=True)
    except Exception as e:
        print(f"⚠️ Telegram Fehler: {e}", flush=True)

    # Discord
    try:
        send_discord(market, network, comparison, news)
        print("💬 Discord erfolgreich gesendet", flush=True)
    except Exception as e:
        print(f"⚠️ Discord Fehler: {e}", flush=True)

    # X (Twitter) Thread
    try:
        send_x_thread(
            report, tokenomics, dusd, network,
            intelligence, current_history, global_crypto, market
        )
        print("🐦 X Thread erfolgreich ausgeführt", flush=True)
    except Exception as e:
        print(f"⚠️ X Fehler: {e}", flush=True)

    print("✅ v5 Report vollständig gesendet!", flush=True)


# ======================================
# EINSTIEGSPUNKT MIT FEHLER-CATCHER
# ======================================

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"❌ KRITISCHER FEHLER IM BOT-SKRIPT: {err}", flush=True)
        traceback.print_exc()
        sys.exit(1)
