# ======================================
# Language Engine v2
# Daily Language Rotation
# ======================================

import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


STATE_FILE = os.path.join(
    BASE_DIR,
    "language_state.json"
)


# Reihenfolge der täglichen Sprachen

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


    except:

        return {
            "last_language": "ar",
            "last_date": ""
        }



# ======================================
# State speichern
# ======================================

def save_state(state):

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



# ======================================
# Sprache des Tages
# ======================================

def get_next_language():

    state = load_state()


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    # gleiche Sprache am gleichen Tag

    if state.get("last_date") == today:

        return state.get(
            "last_language",
            "en"
        )


    last = state.get(
        "last_language",
        "ar"
    )


    try:

        index = LANGUAGES.index(
            last
        )

    except:

        index = 0



    next_index = (
        index + 1
    ) % len(LANGUAGES)



    language = LANGUAGES[
        next_index
    ]


    state = {

        "last_language": language,

        "last_date": today

    }


    save_state(
        state
    )


    return language
