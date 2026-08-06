# ======================================
# DeFiChain Intelligence v5
# History Engine v2.1
# ======================================

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTENT_FILE = "dfi_content.json"
STATE_FILE = os.path.join(BASE_DIR, "history_state.json")



# ======================================
# History laden
# ======================================

def load_content():

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception as e:

        print(
            "History Load Fehler:",
            e
        )

        return []



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
            "last_id": 0,
            "last_title": ""
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
            "History State Fehler:",
            e
        )



# ======================================
# Intelligentes Kapitel auswählen
# ======================================

def get_history():


    history = load_history()


    if not history:

        return None



    state = load_state()



    try:

        last_id = int(
            state.get(
                "last_id",
                0
            )
        )

    except:

        last_id = 0



    next_id = last_id + 1



    # Nach Kapitel 100 wieder von vorne

    if next_id > len(history):

        next_id = 1



    current = None



    for chapter in history:


        if chapter.get("id") == next_id:

            current = chapter

            break



    # Falls Kapitel nicht gefunden

    if current is None:

        current = history[0]



    # Fortschritt speichern

    state["last_id"] = current.get(
        "id",
        1
    )


    state["last_title"] = current.get(
        "title",
        ""
    )


    save_state(state)



    return current
