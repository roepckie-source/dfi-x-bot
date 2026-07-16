import os
import requests
from datetime import datetime


# Discord Webhook aus GitHub Secrets laden
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


# DFI Preis von CoinGecko abrufen
def get_dfi_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        "ids": "defichain",
        "vs_currencies": "usd,eur",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    dfi = data["defichain"]

    return (
        dfi["usd"],
        dfi["eur"],
        dfi.get("usd_24h_change", 0)
    )


# Discord Nachricht senden
def send_discord(message):
    response = requests.post(
        DISCORD_WEBHOOK,
        json={
            "content": message
        }
    )

    if response.status_code == 204:
        print("Discord Nachricht erfolgreich gesendet")
    else:
        print("Discord Fehler:")
        print(response.text)

# Hauptprogramm
try:
    dfi_usd, dfi_eur, change = get_dfi_price()

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    emoji = "🟢" if change >= 0 else "🔴"

    message = f"""
🚀 **DeFiChain DFI Update**

💰 **DFI Preis**
🇺🇸 USD: ${dfi_usd:.6f}
🇪🇺 EUR: €{dfi_eur:.6f}

{emoji} **24h Änderung:** {change:.2f}%

🕒 Zeit:
{now}

🔗 https://defichain.com
"""

    send_discord(message)


except Exception as e:
    print("Fehler:")
    print(e)
