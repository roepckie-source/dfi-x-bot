import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Setzt das Hauptverzeichnis (Root) garantiert in den Python-Suchpfad
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Modul-Imports
from modules.community import get_community_data
from modules.dusd import get_dusd_data
from modules.global_crypto import get_global_crypto
from modules.history_engine import get_history_chapter
from modules.insight_engine import generate_daily_insight
from modules.intelligence import calculate_intelligence_score
from modules.language import load_language
from modules.market import get_market_data
from modules.network import get_network_data
from modules.tokenomics import get_tokenomics_data

# Output-Imports
from outputs.discord_bot import send_discord
from outputs.telegram_bot import send_telegram
from outputs.x_bot import send_x_thread

# Liste der unterstützen Sprachen für die tägliche Rotation
SUPPORTED_LANGUAGES = ["de", "en", "es", "fr", "pt", "ru"]
STATE_FILE = ROOT_DIR / "language_state.json"


def get_next_language():
    """Liest die zuletzt genutzte Sprache aus und ermittelt die nächste in der Reihe."""
    last_index = -1

    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                last_lang = data.get("last_language", "")
                if last_lang in SUPPORTED_LANGUAGES:
                    last_index = SUPPORTED_LANGUAGES.index(last_lang)
        except Exception as e:
            print(f"⚠️ Fehler beim Lesen von {STATE_FILE.name}: {e}")

    # Nächsten Index ermitteln (mit Rotationsprinzip)
    next_index = (last_index + 1) % len(SUPPORTED_LANGUAGES)
    next_lang = SUPPORTED_LANGUAGES[next_index]

    # Neuen Zustand speichern
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_language": next_lang}, f, indent=2)
    except Exception as e:
        print(f"⚠️ Fehler beim Speichern von {STATE_FILE.name}: {e}")

    return next_lang


def main():
    print("🚀 DeFiChain Intelligence v5 startet...")

    # 1. Automatische Sprachauswahl (Rotation)
    # Falls APP_LANG manuell übergeben wird, hat diese Vorrang
    lang_code = os.getenv("APP_LANG")
    if not lang_code:
        lang_code = get_next_language()

    lang_data = load_language(lang_code)
    print(f"🌍 Aktuelle Sprache für diesen Lauf: {lang_code.upper()}")

    # 2. Daten aus den Modulen abrufen
    global_data = get_global_crypto()
    market_data = get_market_data()
    tokenomics_data = get_tokenomics_data()
    dusd_data = get_dusd_data()
    community_data = get_community_data()
    network_data = get_network_data()

    # 3. Intelligence Score berechnen
    score_data = calculate_intelligence_score(
        market_data, tokenomics_data, dusd_data, community_data, network_data
    )

    # 4. Historischen Kontext & Insights laden
    history_chapter = get_history_chapter()
    daily_insight = generate_daily_insight(lang_code)

    # Werte für die Berichterstellung aufbereiten
    if isinstance(score_data, dict):
        score_val = score_data.get("score", 0)
        status_val = score_data.get(
            "status", lang_data.get("status_vorsicht", "🟠 Caution")
        )
    else:
        score_val = score_data
        status_val = lang_data.get("status_vorsicht", "🟠 Caution")

    if isinstance(history_chapter, dict):
        history_title = history_chapter.get("title", "")
    else:
        history_title = str(history_chapter)

    # Marktpreise extrahieren
    dfi_price = (
        market_data.get("price", 0.0) if isinstance(market_data, dict) else 0.0
    )
    dfi_change = (
        market_data.get("change_24h", 0.0)
        if isinstance(market_data, dict)
        else 0.0
    )

    btc_price = (
        global_data.get("bitcoin", {}).get("price", 0)
        if isinstance(global_data, dict)
        else 0
    )
    eth_price = (
        global_data.get("ethereum", {}).get("price", 0)
        if isinstance(global_data, dict)
        else 0
    )

    # Zeitstempel zur Identifikation
    current_date = datetime.now().strftime("%d.%m.%Y")

    # 5. Vollständigen Bericht in der jeweiligen Tagessprache zusammensetzen
    full_report = (
        f"{lang_data.get('header_title', '🚀 DeFiChain Intelligence')} ({current_date})\n"
        f"{lang_data.get('header_line1', '')}\n"
        f"-----------------------------------------\n\n"
        f"💰 {lang_data.get('market', 'Market')}:\n"
        f"• DFI: ${dfi_price:.4f} USD ({dfi_change:+.2f}%)\n"
        f"• BTC: ${btc_price:,.0f} USD | ETH: ${eth_price:,.0f} USD\n\n"
        f"🧠 {lang_data.get('intelligence', 'DFI INTELLIGENCE INDEX')}: {score_val} / 100\n"
        f"{status_val}\n\n"
        f"💡 {lang_data.get('insight', 'Daily Insight')}:\n"
        f"{daily_insight}\n\n"
        f"📚 {lang_data.get('history', 'History')}: {history_title}\n"
        f"-----------------------------------------\n"
        f"{lang_data.get('header_line2', '')}"
    )

    print("\n--- ERSTELLTER BERICHT ---")
    print(full_report)
    print("--------------------------\n")

    # 6. Telegram-Versand
    telegram_success = send_telegram(full_report)
    if telegram_success:
        print("✅ Telegram erfolgreich gesendet")
    else:
        print("❌ Fehler beim Versenden an Telegram")

    # 7. Discord-Versand
    comparison_payload = (
        market_data if isinstance(market_data, dict) else {"dfi": {}}
    )
    if "dfi" not in comparison_payload and isinstance(market_data, dict):
        comparison_payload = {"dfi": market_data}

    discord_success = send_discord(
        full_report, network_data, comparison_payload, ""
    )
    if discord_success:
        print("✅ Discord erfolgreich gesendet")
    else:
        print("⚠️ Discord nicht gesendet oder übersprungen")

    # 8. X (Twitter)-Versand
    x_success = send_x_thread(
        full_report,
        tokenomics_data,
        dusd_data,
        network_data,
        score_data,
        history_chapter,
        global_data,
        comparison_payload,
    )
    if x_success:
        print("🎉 X Thread erfolgreich gesendet!")
    else:
        print("⚠️ X Thread nicht gesendet oder übersprungen")

    print(
        f"✅ v5 Report-Prozess beendet ({lang_code.upper()} erfolgreich verarbeitet)"
    )


if __name__ == "__main__":
    main()
