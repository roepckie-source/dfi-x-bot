import json
import os


HISTORY_FILE = "dfi_history.json"
STATE_FILE = "news_state.json"


# ==============================
# DFI HISTORY LADEN
# ==============================

def load_history():

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception as e:

        print(
            "History Fehler:",
            e
        )

        return []



# ==============================
# STATUS LADEN
# ==============================

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
            "last_history_id": 0
        }



# ==============================
# STATUS SPEICHERN
# ==============================

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



# ==============================
# NÄCHSTE GESCHICHTE
# ==============================

def get_history_story():

    history = load_history()

    state = load_state()


    if not history:

        return {

            "title": "DeFiChain Update",

            "text": "No history available."

        }



    last_id = state.get(
        "last_history_id",
        0
    )


    next_story = None


    for story in history:

        if story["id"] > last_id:

            next_story = story

            break



    # Wenn Ende erreicht -> wieder von vorne

    if next_story is None:

        next_story = history[0]



    state["last_history_id"] = next_story["id"]


    save_state(state)



    return {

        "title": next_story["title"],

        "text": next_story["text"],

        "hashtags": "#DeFiChain #DFI"

    }



# ==============================
# NEWS FUNKTION
# ==============================

def get_news():

    return get_history_story()


# ==============================
# KOMPATIBILITÄT FÜR MAIN.PY
# ==============================

def get_dfi_news():

    return get_history_story()
