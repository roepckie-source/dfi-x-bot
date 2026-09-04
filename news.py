# ==============================================================
# DeFiChain Bot News Module - news.py
# Schnittstelle zur zentralen modules/history_engine.py
# ==============================================================

from modules.history_engine import get_history_text


def get_dfi_news(lang="de"):
  """Hauptschnittstelle für main.py – liefert den aktuellen Nachrichtentext aus der History-Engine als String."""
  return get_history_text(lang)


def get_news(lang="de"):
  """Alternative Schnittstelle für Kompatibilität mit anderen Skripten."""
  return get_history_text(lang)
