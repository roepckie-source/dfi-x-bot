import os
import requests
# Korrigierter Import: 'insights' statt 'insight'
from modules.insight_engine import generate_daily_insight


def send_telegram(message: str) -> bool:
    """Sendet eine Nachricht an den konfigurierten Telegram-Chat."""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram Token oder Chat ID fehlt in den Umgebungsvariablen.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Telegram erfolgreich gesendet")
        return True
    except Exception as e:
        print(f"Fehler beim Senden an Telegram: {e}")
        return False
