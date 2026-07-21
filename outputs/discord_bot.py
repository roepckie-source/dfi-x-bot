import requests
from config import DISCORD_WEBHOOK
from utils import format_percent, format_large_number


# ==============================
# DISCORD REPORT
# ==============================


def send_discord(
    market,
    network,
    comparison,
    news
):


    if not DISCORD_WEBHOOK:

        print(
            "Kein Discord Webhook vorhanden"
        )

        return



    dfi = market["dfi"]

    btc = market["bitcoin"]

    eth = market["ethereum"]



    message = f"""

🚀 **DeFiChain Daily Update**


💰 **DFI**

${dfi.get('usd',0):.8f}

🇪🇺 €{dfi.get('eur',0):.8f}


{format_percent(
    dfi.get('usd_24h_change',0)
)}


📊 **Market Cap**

${format_large_number(
    dfi.get('usd_market_cap',0)
)}


🌍 **Market Comparison**


₿ Bitcoin:

{format_percent(
    btc.get('usd_24h_change',0)
)}


Ξ Ethereum:

{format_percent(
    eth.get('usd_24h_change',0)
)}


{comparison['vs_btc']}

{comparison['vs_eth']}



🌐 **Network**


🔥 Burned DFI:

{network['burned_dfi']}


🔒 Locked dUSD:

{network['locked_dusd']}



📰 **News**

{news['title']}

{news['text']}


{news['hashtags']}

"""


    try:

        response = requests.post(

            DISCORD_WEBHOOK,

            json={
                "content": message
            },

            timeout=20

        )


        if response.status_code == 204:

            print(
                "Discord erfolgreich gesendet"
            )

        else:

            print(
                "Discord Fehler:",
                response.text
            )


    except Exception as e:

        print(
            "Discord Ausnahme:",
            e
        )

