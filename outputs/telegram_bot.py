# ======================================
# DeFiChain Intelligence v5
# Telegram Bot Module
# ======================================

import os
import re
import requests
from modules.language import load_language


# ======================================
# FORMAT HELFER
# ======================================

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_change(value):
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "0.00"


def format_price(value):
    try:
        value = float(value)
        if value < 0.01:
            return f"{value:.8f}"
        if value < 1:
            return f"{value:.6f}"
        if value < 100:
            return f"{value:.2f}"
        return f"{value:,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def format_large_number(value, suffix=""):
    try:
        val = float(value)
        if val >= 1_000_000_000:
            return f"{val / 1_000_000_000:.2f}B{suffix}"
        if val >= 1_000_000:
            return f"{val / 1_000:.2f}M{suffix}"
        if val >= 1_000:
            return f"{val / 1_000:.1f}K{suffix}"
        return f"{val:,.2f}{suffix}"
    except (ValueError, TypeError):
        return str(value) if value else "N/A"


def change_emoji(value):
    try:
        return "🟢" if float(value) >= 0 else "🔴"
    except (TypeError, ValueError):
        return "⚪"


def detect_language(insight):
    if isinstance(insight, str):
        match = re.search(r"\(([A-Z]{2})\)", insight)
        if match:
            return match.group(1).lower()
    return os.getenv("APP_LANG", "de")


# ======================================
# BASIC TELEGRAM SEND
# ======================================

def send_telegram(text):
    """Greift sowohl TELEGRAM_BOT_TOKEN als auch TELEGRAM_TOKEN ab."""
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Telegram Token oder Chat ID fehlt in den Umgebungsvariablen.", flush=True)
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("🤖 Telegram Nachricht erfolgreich gesendet", flush=True)
            return True
        else:
            print(f"❌ Telegram API Fehler: {response.status_code} - {response.text}", flush=True)
            return False
    except Exception as e:
        print(f"❌ Ausnahmefehler bei Telegram: {e}", flush=True)
        return False


# ======================================
# HIGH-LEVEL REPORT FUNCTION
# ======================================

def send_telegram_report(
    insight="",
    tokenomics=None,
    dusd=None,
    network=None,
    intelligence=None,
    current_history=None,
    global_crypto=None,
    market=None
):

    language = detect_language(insight)
    lang = load_language(language)

    if not isinstance(intelligence, dict):
        intelligence = {}
    if not isinstance(global_crypto, dict):
        global_crypto = {}
    if not isinstance(market, dict):
        market = {}
    if not isinstance(network, dict):
        network = {}
    if not isinstance(tokenomics, dict):
        tokenomics = {}

    # Markt Daten
    btc = global_crypto.get("bitcoin", {})
    eth = global_crypto.get("ethereum", {})
    dfi = market.get("dfi", {})

    btc_price = btc.get("price", "N/A")
    btc_change = safe_float(btc.get("change", 0))

    eth_price = eth.get("price", "N/A")
    eth_change = safe_float(eth.get("change", 0))

    dfi_price = dfi.get("price", dfi.get("usd", "N/A"))
    dfi_change = safe_float(dfi.get("change", 0))

    # Flexible Key-Abfrage für Tokenomics
    burned_dfi_raw = (
        tokenomics.get("burned_dfi") 
        or tokenomics.get("burned") 
        or tokenomics.get("total_burned") 
        or tokenomics.get("dfi_burned")
    )
    daily_minted_raw = (
        tokenomics.get("daily_minted") 
        or tokenomics.get("minted_24h") 
        or tokenomics.get("minted") 
        or tokenomics.get("daily_emission")
    )

    burned_dfi = format_large_number(burned_dfi_raw) if burned_dfi_raw else "N/A"
    daily_minted = format_large_number(daily_minted_raw) if daily_minted_raw else "N/A"

    score = intelligence.get("total", "N/A")
    status = intelligence.get("status", "N/A")
    daily_insight = intelligence.get("daily_insight", "")

    header_title = lang.get("header_title", "🚀 DeFiChain Daily Intelligence")

    # Telegram HTML Formatted Message
    msg = f"""
<b>{header_title}</b> ({language.upper()})

🌍 <b>Global Crypto</b>
• ₿ BTC: ${format_price(btc_price)} ({change_emoji(btc_change)} {safe_change(btc_change)}%)
• Ξ ETH: ${format_price(eth_price)} ({change_emoji(eth_change)} {safe_change(eth_change)}%)

💎 <b>DeFiChain (DFI)</b>
• 💵 Preis: ${format_price(dfi_price)} ({change_emoji(dfi_change)} {safe_change(dfi_change)}%)
• 🔥 Verbrannt: {burned_dfi} DFI
• 🪙 Täglich gemintet: {daily_minted} DFI

🧠 <b>Intelligence Score:</b> {score}/100 ({status})

💡 <b>Daily Insight:</b>
{daily_insight}

#DeFiChain #DFI
""".strip()

    return send_telegram(msg)
