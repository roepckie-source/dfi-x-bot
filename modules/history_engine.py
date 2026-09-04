# ======================================
# DeFiChain Intelligence v5
# History Engine v2.3 (Includes Chapter Metadata)
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


def get_history(lang="de"):
  history = load_history()
  if not history:
    return None

  state = load_state()

  try:
    last_id = int(state.get("last_id", 0))
  except (ValueError, TypeError):
    last_id = 0

  next_id = last_id + 1

  if next_id > len(history):
    next_id = 1

  current = None

  for chapter in history:
    try:
      chap_id = int(chapter.get("id"))
      if chap_id == next_id:
        current = chapter
        break
    except (ValueError, TypeError):
      continue

  if current is None:
    current = history[0]

  try:
    state["last_id"] = int(current.get("id", 1))
  except (ValueError, TypeError):
    state["last_id"] = 1

  title_val = current.get("title", "")
  if isinstance(title_val, dict):
    state["last_title"] = title_val.get(lang, title_val.get("de", ""))
  else:
    state["last_title"] = str(title_val)

  save_state(state)

  return current


def get_history_text(lang="de"):
  """Gibt den formatierten Text inklusive Tag-Anzahl (z. B. Tag 2/100) zurück."""
  history = load_history()
  total_count = len(history) if history else 100
  chapter = get_history(lang)

  if not chapter:
    return "Keine besonderen Ereignisse im Ökosystem."

  chap_id = chapter.get("id", 1)

  text_data = chapter.get("text", "")
  if isinstance(text_data, dict):
    story_text = text_data.get(lang, text_data.get("de", ""))
  else:
    story_text = str(text_data)

  label = "Tag" if lang.lower() == "de" else "Day"
  return f"[{label} {chap_id}/{total_count}]\n{story_text}"


# Aliase für Kompatibilität
get_history_chapter = get_history
get_next_history_story = get_history_text
get_dfi_news = get_history_text
