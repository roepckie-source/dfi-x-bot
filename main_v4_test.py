import os
import sys
from pathlib import Path

# Setzt das Hauptverzeichnis (Root) garantiert in den Python-Suchpfad
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Modul-Imports mit korrekten Funktionsnamen
from modules.language import load_language
from modules.global_crypto import get_global_crypto  # Korrigiert: get_global_crypto
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

    # 3. Intelligence Score berechnen
    score_data = calculate_intelligence_score()
    print(f"🧠 Intelligence Score: {score_data.get('score')} /100")
    print(f"🟠 {score_data.get('status')}")

    # 4. Historischen Kontext & Insights laden
    history_chapter = get_history_chapter()
    print(f"📚 History: {history_chapter.get('title', '')}")

    daily_insight = generate_daily_insight()
    print("💡 Daily Insight:")
    print(daily_insight)

    # 5. Benachrichtigungen versenden
    telegram_success = send_telegram(daily_insight)
    if telegram_success:
        print("Telegram erfolgreich gesendet")

    discord_success = send_discord(daily_insight)
    if discord_success:
        print("Discord erfolgreich gesendet")

    x_success = send_x_thread(daily_insight)
    if x_success:
        print("🎉 X Thread erfolgreich gesendet!")

    print("✅ v5 Report gesendet")


if __name__ == "__main__":
    main()
