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
# Sprachreihenfolge
# ======================================

LANGUAGES = [
    "en",
    "de",
    "es",
    "fr",
    "pt",
    "ru",
    "ja",
    "zh",
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

        return {
            "last_language": "en",
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

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    # ==================================
    # Gleiche Sprache am gleichen Tag
    # ==================================

    if state.get("last_date") == today:

        return state.get(
            "last_language",
            "en"
        )


    # ==================================
    # Letzte Sprache
    # ==================================

    last = state.get(
        "last_language",
        "en"
    )


    try:

        index = LANGUAGES.index(
            last
        )

    except ValueError:

        index = 0


    # ==================================
    # Nächste Sprache
    # ==================================

    next_index = (
        index + 1
    ) % len(LANGUAGES)


    language = LANGUAGES[
        next_index
    ]


    # ==================================
    # State aktualisieren
    # ==================================

    state = {

        "last_language": language,

        "last_date": today

    }


    save_state(
        state
    )


    print(
        f"🌐 Sprache gespeichert: {language}"
    )

    print(
        f"📅 Datum gespeichert: {today}"
    )


    return language
