# ======================================
# DeFiChain Intelligence v5
# History Engine
# Daily DeFiChain Education Series
# ======================================


import json
import os



# Dateien

HISTORY_FILE = "dfi_news.json"

STATE_FILE = "news_state.json"





# ======================================
# History laden
# ======================================


def load_history():


    try:

        with open(

            HISTORY_FILE,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)



    except Exception as e:


        print(

            "History Laden Fehler:",

            e

        )


        return []






# ======================================
# Status laden
# ======================================


def load_state():


    try:


        with open(

            STATE_FILE,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)



    except:


        return {

            "last_id": 0

        }






# ======================================
# Status speichern
# ======================================


def save_state(state):


    try:


        with open(

            STATE_FILE,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                state,

                f,

                indent=2,

                ensure_ascii=False

            )



    except Exception as e:


        print(

            "State speichern Fehler:",

            e

        )






# ======================================
# Nächstes Kapitel
# ======================================


def get_daily_history():



    history = load_history()



    if not history:


        return None




    state = load_state()



    last_id = state.get(

        "last_id",

        0

    )



    next_id = last_id + 1




    # Wenn Ende erreicht -> wieder von vorne

    if next_id > len(history):


        next_id = 1




    chapter = None




    for item in history:


        if item.get("id") == next_id:


            chapter = item

            break




    if chapter:



        state["last_id"] = next_id


        save_state(state)



        return chapter




    return None
