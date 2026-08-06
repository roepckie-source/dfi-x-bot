# ======================================
# DeFiChain Intelligence v5
# Content Engine v1
# ======================================

import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CONTENT_FILE = "dfi_content.json"

STATE_FILE = os.path.join(
    BASE_DIR,
    "history_state.json"
)


# ======================================
# Content laden
# ======================================

def load_content():

    try:

        with open(
            os.path.join(
                BASE_DIR,
                CONTENT_FILE
            ),
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception as e:

        print(
            "Content Load Fehler:",
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
            "Content State Fehler:",
            e
        )



# ======================================
# Nächsten Content auswählen
# ======================================

def get_content():

    content = load_content()


    if not content:

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



    # Wenn Ende erreicht -> wieder vorne beginnen

    if next_id > len(content):

        next_id = 1



    current = None



    for item in content:


        if item.get("id") == next_id:

            current = item

            break



    # Falls Kapitel fehlt

    if current is None:

        current = content[0]



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
