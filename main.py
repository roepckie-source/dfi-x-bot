import os
import tweepy
import requests
from datetime import datetime

# X API Zugangsdaten aus GitHub Secrets laden


# X Verbindung herstellen


# DFI Preis abrufen
def get_dfi_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=defichain&vs_currencies=usd"
    data = requests.get(url).json()
    return data["defichain"]["usd"]

# Post erstellen
price = get_dfi_price()

message = (
    f"🚀 DeFiChain Daily Update\n\n"
    f"DFI Preis: ${price}\n\n"
    f"#DeFiChain #DFI\n"
    f"{datetime.now().strftime('%d.%m.%Y')}"
)

# X Verbindung testen
me = client.get_me()

print("X Verbindung erfolgreich")
print(me.data)

# Tweet senden

# Discord Nachricht senden
import requests

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

message = f"""
🚀 DeFiChain DFI Update

💰 DFI Preis: {dfi_price} USD

🕒 Zeitpunkt:
{datetime.now().strftime("%d.%m.%Y %H:%M")}

🔗 DeFiChain:
https://defichain.com
"""

response = requests.post(
    DISCORD_WEBHOOK,
    json={"content": message}
)

if response.status_code == 204:
    print("Discord Nachricht erfolgreich gesendet")
else:
    print("Discord Fehler:", response.text)



