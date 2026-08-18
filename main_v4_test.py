import os
import sys
from pathlib import Path

# Setzt das Hauptverzeichnis (Root) garantiert in den Python-Suchpfad
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Modul-Imports
from modules.language import load_language
from modules.global_crypto import get_global_crypto
from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.network import get_network_data
from modules.intelligence import calculate_intelligence_score
from modules.history_engine import get_history_chapter
from modules.insight_engine import generate_daily_insight

# Output-Imports
from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread


def main():
    print("🚀 DeFiChain Intelligence v5 startet...")

    # 1. Sprache laden
    lang_code = os.getenv("APP_LANG", "ru")
    lang_data = load_language(lang_code)
    print(f"🌍 Sprache: {lang_code}")

    # 2. Globale Marktdaten abrufen
    global_data = get_global_crypto()
    print("🌍 Global Crypto:")
    print(global_data)

    # 3. Teil-Metriken aus allen Modulen laden
    market_data = get_market_data()
    tokenomics_data = get_tokenomics_data()
    dusd_data = get_dusd_data()
    community_data = get_community_data()
    network_data = get_network_data()

    # 4. Intelligence Score berechnen
    score_data = calculate_intelligence_score(
        market_data,
        tokenomics_data,
        dusd_data,
        community_data,
        network_data
    )

    if isinstance(score_data, dict):
        print(f"🧠 Intelligence Score: {score_data.get('score', 0)} /100")
        print(f"🟠 {score_data.get('status', '')}")
    else:
        print(f"🧠 Intelligence Score: {score_data} /100")

    # 5. Historischen Kontext & Insights laden
    history_chapter = get_history_chapter()
    if isinstance(history_chapter, dict):
        print(f"📚 History: {history_chapter.get('title', '')}")
    else:
        print(f"📚 History: {history_chapter}")

    daily_insight = generate_daily_insight()
    print("💡 Daily Insight:")
    print(daily_insight)

    # 6. Benachrichtigungen versenden
    telegram_success = send_telegram(daily_insight)
    if telegram_success:
        print("Telegram erfolgreich gesendet")

    # FIX: send_discord erwartet (insight, network, comparison, news)
    discord_success = send_discord(
        daily_insight, 
        network_data, 
        market_data, 
        ""
    )
    if discord_success:
        print("Discord erfolgreich gesendet")

    x_success = send_x_thread(daily_insight)
    if x_success:
        print("🎉 X Thread erfolgreich gesendet!")

    print("✅ v5 Report gesendet")


if __name__ == "__main__":
    main()
