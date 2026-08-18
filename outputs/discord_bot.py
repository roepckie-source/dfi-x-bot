import os
import requests


def send_discord(insight, network, comparison, news):
    """Versendet den Bericht an Discord via Webhook und fängt Typ-Fehler bei 'comparison' ab."""
    
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ DISCORD_WEBHOOK_URL nicht gesetzt.")
        return False

    # 1. Typ-Sicherung für 'comparison' / 'market'
    if isinstance(comparison, dict):
        dfi_data = comparison.get("dfi", {})
        # Falls comparison['dfi'] kein Dict ist
        if not isinstance(dfi_data, dict):
            dfi_data = {}
    else:
        # Fallback, falls ein String übergeben wurde
        dfi_data = {}

    # 2. Sichere Datenextrahierung mit Default-Werten
    price = dfi_data.get("price", "N/A")
    change_24h = dfi_data.get("change", "N/A")

    # 3. Embed / Nachricht aufbauen
    embed_content = {
        "title": "🚀 DeFiChain Daily Intelligence Report",
        "description": str(insight),
        "color": 3447003,  # Blau
        "fields": [
            {
                "name": "📊 Market Info",
                "value": f"Price: {price} | 24h Change: {change_24h}",
                "inline": False
            },
            {
                "name": "⛓ Network Status",
                "value": str(network) if network else "Normal",
                "inline": True
            }
        ],
        "footer": {
            "text": "DeFiChain Intelligence Bot v5"
        }
    }

    payload = {
        "username": "DeFiChain Intelligence",
        "embeds": [embed_content]
    }

    # 4. An Discord senden
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            return True
        else:
            print(f"❌ Discord Webhook Fehler Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Fehler beim Senden an Discord: {e}")
        return False
