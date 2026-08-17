# ======================================
# DeFiChain Intelligence v5
# Telegram Bot Output (Language-Aware & Complete)
# ======================================

import os
import requests
from modules.language import load_language
from modules.insight import generate_insights


def send_telegram_message(
    market,
    tokenomics,
    dusd,
    network,
    intelligence,
    current_history,
    global_crypto,
    comparison,
    news=None,
    language="de",
    lang_data=None,
):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Telegram Credentials fehlen!")
        return

    if not lang_data:
        lang_data = load_language(language)

    # --------------------------------------------------
    # DFI Preis auslesen (robuste Erkennung)
    # --------------------------------------------------
    dfi_raw = market.get("dfi", {})
    dfi_data = dfi_raw.get("dfi", {}) if isinstance(dfi_raw, dict) and "dfi" in dfi_raw else dfi_raw

    dfi_price = (
        dfi_data.get("price")
        or dfi_data.get("price_usd")
        or dfi_data.get("usd")
        or dfi_data.get("last_price")
        or "N/A"
    )
    dfi_change = dfi_data.get("change", 0) if isinstance(dfi_data, dict) else 0
    dfi_emoji = "🟢" if dfi_change >= 0 else "🔴"

    # Status-Übersetzung aus Sprachdatei
    score_val = intelligence.get("total", 0)
    raw_status = intelligence.get("status", "Vorsicht")
    status_translated = lang_data.get(f"status_{raw_status.lower()}", raw_status)

    # --------------------------------------------------
    # History zusammenbauen (Titel + Erklärungstext)
    # --------------------------------------------------
    hist_title = "N/A"
    hist_text = ""
    hist_id = ""

    if current_history and isinstance(current_history, dict):
        hist_title = current_history.get("title", "N/A")
        hist_text = (
            current_history.get("content")
            or current_history.get("text")
            or current_history.get("description")
            or ""
        )
        hist_id = current_history.get("id", "")

    history_str = f"📚 {lang_data.get('history', 'History')}:"
    if hist_id:
        history_str += f" Ch.{hist_id}: {hist_title}"
    else:
        history_str += f" {hist_title}"

    if hist_text:
        history_str += f'\n"{hist_text}"'

    # Insights generieren
    insights_str = generate_insights(market, tokenomics, dusd, network, language, lang_data)

    # Flaggen-Symbol
    flag_map = {
        "de": "DE", "en": "EN", "ru": "RU", "es": "ES",
        "fr": "FR", "pt": "PT", "ja": "JA", "hi": "HI",
        "id": "ID", "ar": "AR", "zh": "ZH"
    }
    lang_code = flag_map.get(language, language.upper())

    # --------------------------------------------------
    # Nachrichten-Layout
    # --------------------------------------------------
    msg = f"{lang_data.get('header_title', '🚀 DeFiChain Intelligence')} ({lang_code})\n"
    msg += f"{lang_data.get('header_line1', '🌍 Global')}\n"
    msg += f"{lang_data.get('header_line2', '')}\n\n"

    msg += f"📊 {lang_data.get('market', 'Market')}: DFI ${dfi_price} ({dfi_emoji} {dfi_change:+.2f}%)\n"
    msg += f"🧠 {lang_data.get('score', 'Score')}: {score_val}/100 ({status_translated})\n\n"

    msg += f"💡 {lang_data.get('insight', 'Daily Insight')}:\n"
    msg += f"{insights_str}\n\n"

    msg += f"{history_str}"

    # Telegram API Call
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}

    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("Telegram erfolgreich gesendet")
        else:
            print(f"❌ Telegram Fehler: {res.status_code} - {res.text}")
    except Exception as e:
        print("❌ Telegram Ausnahmefehler:", e)
