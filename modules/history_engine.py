# ======================================
# DeFiChain Intelligence v5
# History Engine v2.2 (Fix: Type-Safe Rotation)
# ======================================

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HISTORY_FILE = os.path.join(BASE_DIR, "dfi_history.json")
STATE_FILE = os.path.join(BASE_DIR, "history_state.json")


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print("History Load Fehler:", e)
        return []


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {"last_id": 0, "last_title": ""}


def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print("History State Fehler:", e)


def get_history():
    history = load_history()
    if not history:
        return None

    state = load_state()

    try:
        last_id = int(state.get("last_id", 0))
    except (ValueError, TypeError):
        last_id = 0

    next_id = last_id + 1

    # Nach dem letzten Kapitel wieder bei 1 starten
    if next_id > len(history):
        next_id = 1

    current = None

    # Typ-sicherer Vergleich (wandelt Strings in Integer um)
    for chapter in history:
        try:
            chap_id = int(chapter.get("id"))
            if chap_id == next_id:
                current = chapter
                break
        except (ValueError, TypeError):
            continue

    # Fallback auf erstes Kapitel, falls ID nicht existiert
    if current is None:
        current = history[0]

    # Fortschritt speichern
    try:
        state["last_id"] = int(current.get("id", 1))
    except (ValueError, TypeError):
        state["last_id"] = 1

    state["last_title"] = current.get("title", "")
    save_state(state)

    return current
