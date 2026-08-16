
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_language(language="de"):
    file_path = os.path.join(BASE_DIR, "languages", f"{language}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"⚠️ Language Load Fehler für '{language}':", e)
        return {}
