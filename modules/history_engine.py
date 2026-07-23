# ======================================
# DeFiChain Intelligence v5
# History Engine v2
# ======================================

import json
import os


HISTORY_FILE = "dfi_history.json"
STATE_FILE = "history_state.json"



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
            "History Load Fehler:",
            e
        )

        return []




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

            "last_id": 0

        }




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




def get_history():

    history = load_history()


    if not history:

        return None



    state = load_state()


    last_id = state.get(
        "last_id",
        0
    )



    next_id = last_id + 1



    # nach Kapitel 100 wieder von vorne

    if next_id > len(history):

        next_id = 1



    chapter = None



    for item in history:

        if item.get("id") == next_id:

            chapter = item

            break



    if chapter is None:

        chapter = history[0]



    # Fortschritt speichern

    state["last_id"] = next_id

    save_state(state)



    return chapter
