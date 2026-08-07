import os
import requests

from modules.language import load_language

# ==============================
# TELEGRAM CONFIG
# ==============================

TELEGRAM_TOKEN = os.environ.get(
    "TELEGRAM_TOKEN"
)

TELEGRAM_CHAT_ID = os.environ.get(
    "TELEGRAM_CHAT_ID"
)


# ==============================
# SEND TELEGRAM MESSAGE
# ==============================

def send_telegram(message, language="en"):

    try:

        lang = load_language(language)
        
        url = (
            f"https://api.telegram.org/"
            f"bot{TELEGRAM_TOKEN}/sendMessage"
        )


        data = {

            "chat_id": TELEGRAM_CHAT_ID,

            "text": message,

            "parse_mode": "HTML"

        }


        response = requests.post(
            url,
            data=data
        )


        if response.status_code == 200:

            print(
                "Telegram erfolgreich gesendet"
            )

        else:

            print(
                "Telegram Fehler:",
                response.text
            )


    except Exception as e:

        print(
            "Telegram Fehler:",
            e
        )

