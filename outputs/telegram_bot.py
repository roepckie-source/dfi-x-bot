import os
import requests

def send_telegram(text):
    # Greift sowohl TELEGRAM_BOT_TOKEN als auch TELEGRAM_TOKEN ab
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram Token oder Chat ID fehlt in den Umgebungsvariablen.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Telegram erfolgreich gesendet")
            return True
        else:
            print(f"❌ Telegram API Fehler: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ausnahmefehler bei Telegram: {e}")
        return False
