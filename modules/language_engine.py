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


def get_next_language():

    state = load_state()

    today = datetime.now().strftime("%Y-%m-%d")

    last_language = state.get(
        "last_language",
        "en"
    )

    last_date = state.get(
        "last_date",
        ""
    )

    # Bereits heute ausgeführt:
    # gleiche Sprache behalten
    if last_date == today:

        print(
            f"🌐 Sprache bereits für heute: {last_language}"
        )

        return last_language


    # Letzte Sprache suchen

    try:

        index = LANGUAGES.index(
            last_language
        )

    except ValueError:

        index = 0


    # Nächste Sprache

    next_index = (
        index + 1
    ) % len(LANGUAGES)


    language = LANGUAGES[
        next_index
    ]


    # State aktualisieren

    state = {

        "last_language": language,

        "last_date": today

    }


    save_state(
        state
    )


    print(
        f"🌐 Neue Sprache: {language}"
    )

    print(
        f"📅 Datum gespeichert: {today}"
    )


    return language