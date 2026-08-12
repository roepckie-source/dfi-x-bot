# ======================================
# Language Engine
# ======================================

import json
import os
from datetime import datetime


# ======================================
# Pfade
# ======================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATE_FILE = os.path.join(
    BASE_DIR,
    "language_state.json"
)


# ======================================
# Sprachreihenfolge (Genau deine 10 Sprachdateien)
# ======================================

LANGUAGES = [
    "en",
    "de",
    "es",
    "fr",
    "pt",
    "ru",
    "ja",
    "hi",
    "id",
    "ar"
]


# ======================================
# State laden
# ======================================

def load_state():
    try:
        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)
    except Exception:
        # Fallback: Setzt "ar" als Start, damit als Erstes "en" gewählt wird
        return {
            "last_language": "ar",
            "last_date": ""
        }


# ======================================
# State speichern
# ======================================

def save_state(state):
    try:
        with open(
            STATE_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                state,
                file,
                indent=4,
                ensure_ascii=False
            )
    except Exception as e:
        print(
            "Language State Fehler:",
            e
        )


# ======================================
# Sprache des Tages
# ======================================

def get_next_language():
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")

    # ==================================
    # Gleiche Sprache am gleichen Tag
    # ==================================
    if state.get("last_date") == today:
        return state.get(
            "last_language",
            "en"
        )

    # ==================================
    # Letzte Sprache ermitteln
    # ==================================
    last = state.get(
        "last_language",
        "ar"
    )

    try:
        index = LANGUAGES.index(last)
    except ValueError:
        index = len(LANGUAGES) - 1

    # ==================================
    # Nächste Sprache in der Schleife
    # ==================================
    next_index = (index + 1) % len(LANGUAGES)
    language = LANGUAGES[next_index]

    # ==================================
    # State aktualisieren
    # ==================================
    state = {
        "last_language": language,
        "last_date": today
    }

    save_state(state)

    print(f"🌐 Sprache für heute gesetzt: {language.upper()}")
    print(f"📅 Datum gespeichert: {today}")

    return language
