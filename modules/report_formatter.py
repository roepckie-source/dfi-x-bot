# ======================================
# DeFiChain Intelligence v5
# Report Formatter
# ======================================

from modules.language import load_language


def create_report(
    market,
    tokenomics,
    dusd,
    community,
    network,
    intelligence,
    daily_insight,
    current_history,
    global_crypto,
    comparison,
    news=None,
    language="de",
    lang_data=None,
    ):



    # Falls lang_data nicht aus main übergeben wurde, selbst laden
    if not lang_data:
        lang_data = load_language(language)

    # Fallback-Texte, falls ein Key im JSON fehlen sollte
    h_title = lang_data.get("header_title", "🚀 DeFiChain Intelligence")
    h_line1 = lang_data.get("header_line1", "Decentralized. Independent.")
    h_line2 = lang_data.get("header_line2", "Beyond Centralized Control.")

    # Marktdaten
    dfi_price = market.get("dfi", {}).get("price", "N/A")
    dfi_change = market.get("dfi", {}).get("change", 0)
    change_emoji = "🟢" if dfi_change >= 0 else "🔴"

    # Score & Status
    score = intelligence.get("total", 0)
    status = intelligence.get("status", "N/A")

    # History / Kapitel
    hist_title = "N/A"
    hist_content = ""
    if current_history and isinstance(current_history, dict):
        hist_title = current_history.get("title", "N/A")
        hist_content = current_history.get("content", "")

    # Bericht zusammenbauen
    report = f"{h_title} ({language.upper()})\n"
    report += f"{h_line1}\n"
    report += f"{h_line2}\n\n"

    report += f"📊 Market: DFI ${dfi_price} ({change_emoji} {dfi_change:.2f}%)\n"
    report += f"🧠 Score: {score}/100 ({status})\n\n"

    if daily_insight:
        report += f"💡 Insight:\n{daily_insight}\n\n"


    # ==============================
    # NEWS
    # ==============================

    if news:
        report += f"📰 News:\n{news}\n\n"
    if hist_title != "N/A":
        report += f"📚 History: {hist_title}\n{hist_content}\n"

    return report
