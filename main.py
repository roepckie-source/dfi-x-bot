import os
import tweepy
import requests
from datetime import datetime

# X API Zugangsdaten aus GitHub Secrets laden
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

# X Verbindung herstellen
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# DFI Preis abrufen
def get_dfi_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=defichain&vs_currencies=usd"
    data = requests.get(url).json()
    return data["defichain"]["usd"]

price = get_dfi_price()

message = (
    f"🚀 DeFiChain Daily Update\n\n"
    f"💰 DFI Preis: ${price}\n\n"
    f"#DeFiChain #DFI\n"
    f"{datetime.now().strftime('%d.%m.%Y')}"
)

# Verbindung testen
try:
    me = client.get_me()
    print("X Verbindung erfolgreich")
    print(me.data)
except Exception as e:
    print("Fehler bei der X-Verbindung:", e)

# Tweet senden
try:
    client.create_tweet(text=message)
    print("Tweet erfolgreich gesendet")
except Exception as e:
    print("Fehler beim Tweet:", e)

# Discord Nachricht senden
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

discord_message = f"""
🚀 DeFiChain DFI Update

💰 DFI Preis: {price} USD

🕒 Zeitpunkt:
{datetime.now().strftime("%d.%m.%Y %H:%M")}

🔗 https://defichain.com
"""

response = requests.post(
    DISCORD_WEBHOOK,
    json={"content": discord_message}
)

if response.status_code == 204:
    print("Discord Nachricht erfolgreich gesendet")
else:
    print("Discord Fehler:", response.text)
