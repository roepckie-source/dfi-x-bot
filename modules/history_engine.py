# ======================================
# DeFiChain Intelligence - History Engine
# ======================================

import json
import os

HISTORY_STATE_FILE = "history_state.json"

def load_history_state():
    if os.path.exists(HISTORY_STATE_FILE):
        try:
            with open(HISTORY_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"current_day": 1}

def save_history_state(state):
    with open(HISTORY_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def get_history_chapter(day_num, lang="de"):
    file_path = f"locales/{lang}.json"
    if not os.path.exists(file_path):
        file_path = "locales/de.json"
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = data.get("history", {})
            return history.get(str(day_num), None)
    except Exception as e:
        print(f"Fehler beim Laden des Kapitels: {e}")
        return None

def get_dfi_news(lang="de", advance_day=True):
    """
    Holt das aktuelle History-Kapitel. 
    Nur wenn advance_day=True ist, wird der Tageszähler für den nächsten Lauf erhöht.
    """
    state = load_history_state()
    current_day = state.get("current_day", 1)
    
    chapter_text = get_history_chapter(current_day, lang=lang)
    
    # Falls das Kapitel für den aktuellen Tag nicht existiert, auf Tag 1 zurücksetzen
    if chapter_text is None:
        current_day = 1
        chapter_text = get_history_chapter(current_day, lang=lang)
    
    # Der Zähler wird nur erhöht, wenn advance_day explizit True ist (z. B. beim ersten Durchlauf in main.py)
    if advance_day:
        state["current_day"] = current_day + 1
        save_history_state(state)
        
    return chapter_text or ""
