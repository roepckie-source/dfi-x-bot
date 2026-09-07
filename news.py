# ======================================
# DeFiChain Intelligence - news.py Wrapper
# ======================================

from modules.history_engine import (
    get_dfi_news as get_history_news_internal,
    get_history_chapter,
)

def get_dfi_news(lang="de", advance_day=True):
    """
    Wrapper-Funktion, die den Aufruf aus main.py entgegennimmt
    und advance_day an die history_engine weiterreicht.
    """
    return get_history_news_internal(lang=lang, advance_day=advance_day)

# Fallback-Aliase für Rückwärtskompatibilität
get_next_history_story = get_dfi_news
