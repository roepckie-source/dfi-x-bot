# ======================================
# Language Engine
# ======================================

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATE_FILE = os.path.join(BASE_DIR, "language_state.json")

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


def load_state():

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except:

        return {
            "last_language": "en"
        }


def save_state(state):

    with open(STATE_FILE, "w", encoding="utf-8") as file:

        json.dump(
            state,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_next_language():

    state = load_state()

    last = state.get("last_language", "en")

    try:
        index = LANGUAGES.index(last)
    except ValueError:
        index = 0

    next_index = (index + 1) % len(LANGUAGES)

    language = LANGUAGES[next_index]

    state["last_language"] = language

    save_state(state)

    return language
