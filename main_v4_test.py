# History-Abschnitt voll ausschreiben (Kapitel-ID, Titel und vollständiger Text)
    if isinstance(history_chapter, dict):
        chap_id = history_chapter.get("id", "")
        chap_title = history_chapter.get("title", "")
        chap_text = (
            history_chapter.get("description")
            or history_chapter.get("text")
            or history_chapter.get("content")
            or ""
        )
        
        if chap_id:
            history_header = f"• Kapitel {chap_id}: {chap_title}"
        else:
            history_header = f"• {chap_title}"
            
        history_block = history_header
        if chap_text:
            history_block += f"\n  {chap_text}"
    else:
        history_block = f"• {history_chapter}"
