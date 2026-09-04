# ==============================================================
# DeFiChain Bot News & History Module - news.py
# ==============================================================

from datetime import datetime
import json
import os

# Pfade relativ zum Verzeichnis dieser Datei bestimmen (verhindert Pfadfehler auf GitHub Actions)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "dfi_history.json")
STATE_FILE = os.path.join(BASE_DIR, "news_state.json")


# ==============================
# 1. DFI HISTORY LADEN
# ==============================
def load_history():
  """Lädt die Liste der historischen Ereignisse aus der JSON-Datei."""
  try:
    if not os.path.exists(HISTORY_FILE):
      return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
      return json.load(file)
  except Exception as e:
    print("History Fehler:", e)
    return []


# ==============================
# 2. STATUS LADEN & SPEICHERN
# ==============================
def load_state():
  """Lädt den aktuellen Zeiger-Status (last_history_id)."""
  try:
    if not os.path.exists(STATE_FILE):
      return {"last_history_id": 0}
    with open(STATE_FILE, "r", encoding="utf-8") as file:
      return json.load(file)
  except Exception:
    return {"last_history_id": 0}


def save_state(state):
  """Speichert den aktualisierten Zeiger-Status ab."""
  try:
    with open(STATE_FILE, "w", encoding="utf-8") as file:
      json.dump(state, file, indent=4, ensure_ascii=False)
  except Exception as e:
    print("State Speicher-Fehler:", e)


# ==============================
# 3. NÄCHSTE GESCHICHTE HOLEN
# ==============================
def get_history_story(lang="de"):
  """Sucht die nächste Story basierend auf der last_history_id und gibt den Text zurück."""
  history = load_history()
  state = load_state()

  if not history:
    return "Keine besonderen Ereignisse im Ökosystem."

  last_id = state.get("last_history_id", 0)
  next_story = None

  # Nächste Story mit höherer ID als der letzten finden
  for story in history:
    if isinstance(story, dict) and story.get("id", 0) > last_id:
      next_story = story
      break

  # Wenn das Ende der Liste erreicht ist -> wieder von vorne beginnen
  if next_story is None and len(history) > 0:
    next_story = history[0]

  if next_story and isinstance(next_story, dict):
    # Status aktualisieren
    state["last_history_id"] = next_story.get("id", 0)
    save_state(state)

    # Text verarbeiten (unterstützt Strings oder mehrsprachige Dicts)
    text_data = next_story.get("text", "")
    if isinstance(text_data, dict):
      story_text = text_data.get(
          lang, text_data.get("de", "Keine News verfügbar.")
      )
    else:
      story_text = str(text_data)

    return story_text

  return "Keine besonderen Ereignisse im Ökosystem."


# ==============================
# 4. SCHNITTSTELLEN FÜR MAIN.PY
# ==============================
def get_dfi_news(lang="de"):
  """Hauptschnittstelle für main.py – liefert den Nachrichtentext als String."""
  return get_history_story(lang)


def get_news(lang="de"):
  """Alternative Schnittstelle für Kompatibilität."""
  return get_history_story(lang)
