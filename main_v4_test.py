
# ======================================
# DeFiChain Intelligence v5
# Main Runner (Fix: Language & Single-History Call)
# ======================================

from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.community import get_community_data
from modules.blockchain import get_blockchain_data
from modules.global_crypto import get_global_crypto
from modules.language import load_language

from modules.report_formatter import create_report
from modules.intelligence import calculate_intelligence_score
from modules.insight_engine import generate_daily_insight
from modules.content_engine import get_content

from outputs.telegram_bot import send_telegram
from outputs.discord_bot import send_discord
from outputs.x_bot import send_x_thread

from modules.language_engine import get_next_language


def main():
    print("🚀 DeFiChain Intelligence v5 startet...")

    # ==========================
    # 1. Sprache laden & zuweisen
    # ==========================
    language = get_next_language()
    print(f"🌍 Sprache gesetzt: {language}")

    # Sprach-Wörterbuch aus der .json laden
    lang_data = load_language(language)

    # ==========================
    # 2. Marktdaten laden
    # ==========================
    market = get_market_data()
    tokenomics = get_tokenomics_data()
    dusd = get_dusd_data()
    community = get_community_data()
    blockchain = get_blockchain_data()
    global_crypto = get_global_crypto()

    print("🌍 Global Crypto:")
    print(global_crypto)

    # ==========================
    # 3. Intelligence Score
    # ==========================
    intelligence = calculate_intelligence_score(
        market, tokenomics, dusd, community, blockchain
    )
    score = intelligence.get("total", 0)

    if score >= 80:
        status = "🟢 Sehr stark"
    elif score >= 60:
        status = "🟡 Stabil"
    elif score >= 40:
        status = "🟠 Vorsicht"
    else:
        status = "🔴 Kritisch"

    intelligence["status"] = status

    print(f"🧠 Intelligence Score: {score} /100")
    print(status)

    # ==========================
    # 4. History Engine (Nur 1x aufrufen!)
    # ==========================
    current_history = get_content()

    if current_history and isinstance(current_history, dict):
        print(f"📚 History: {current_history.get('title', 'N/A')}")
    else:
        current_history = None
        print("📚 History: keine Daten")

    # ==========================
    # 5. Network Adapter
    # ==========================
    network = {
        "network_status": blockchain.get("network_status", "🟢 Online"),
        "block_height": blockchain.get("block_height", "N/A"),
        "last_block_time": blockchain.get("last_block_time", "N/A"),
        "masternodes": blockchain.get("masternodes", "N/A"),
        "burned_dfi": tokenomics.get("burn", {}).get("total", "N/A"),
        "locked_dusd": dusd.get("locked", "N/A"),
        "excess_dfi": tokenomics.get("balance", "N/A"),
    }

    # ==========================
    # 6. Daily Insight
    # ==========================
    daily_insight = generate_daily_insight(
        market, tokenomics, dusd, community, network, language
    )

    print("💡 Daily Insight:")
    print(daily_insight)

    # ==========================
    # 7. Crypto Comparison
    # ==========================
    dfi_change = float(market.get("dfi", {}).get("change", 0))
    btc_change = float(global_crypto.get("bitcoin", {}).get("change", 0))
    eth_change = float(global_crypto.get("ethereum", {}).get("change", 0))

    comparison = {
        "bitcoin": btc_change,
        "ethereum": eth_change,
        "dfi": dfi_change,
        "vs_btc": btc_change,
        "vs_eth": eth_change,
    }

    # ==========================
    # 8. Report erstellen
    # ==========================
    report = create_report(
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
        language=language,
        lang_data=lang_data,
    )

    # ==========================
    # 9. Outputs
    # ==========================
    send_telegram(report, language)

    send_discord(market, network, comparison, current_history)

    send_x_thread(
        market,
        tokenomics,
        dusd,
        network,
        intelligence,
        current_history,
        global_crypto,
        comparison,
        current_history,
        language=language,
        lang_data=lang_data,
    )

    print("✅ v5 Report gesendet")


if __name__ == "__main__":
    main()
