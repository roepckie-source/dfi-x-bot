# ======================================
# DeFiChain Intelligence v4
# Telegram Report Formatter
# ======================================


from datetime import datetime



def create_report(
        market,
        tokenomics,
        dusd,
        community,
        blockchain
):


    now = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )


    burn = tokenomics.get(
        "burn",
        {}
    )


    emission = tokenomics.get(
        "emission",
        0
    )


    balance = tokenomics.get(
        "burn_vs_emission",
        0
    )


    if balance > 0:

        burn_status = "🟢 Deflationär"

    else:

        burn_status = "🔴 Inflationär"



    report = f"""

🚀 DeFiChain Daily Intelligence


📅 {now}


━━━━━━━━━━━━━━


💰 DFI MARKET


💎 Price

🇺🇸 ${market.get('usd','N/A')}

🇪🇺 €{market.get('eur','N/A')}


📊 24h Change

{market.get('change','N/A')}


━━━━━━━━━━━━━━


🔥 TOKENOMICS


🏠 Address Burn

{burn.get('address','N/A')} DFI


💸 Fee Burn

{burn.get('fee','N/A')} DFI


🔨 Auction Burn

{burn.get('auction','N/A')} DFI


↩️ Payback

{burn.get('payback','N/A')} DFI


🔥 Total Burn

{burn.get('total','N/A')} DFI



📈 Emission

{emission} DFI


⚖️ Burn vs Emission

{burn_status}


━━━━━━━━━━━━━━


🪙 DUSD HEALTH


{dusd}


━━━━━━━━━━━━━━


🏦 COMMUNITY FUND


{community}


━━━━━━━━━━━━━━


⛓ NETWORK


{blockchain}


━━━━━━━━━━━━━━


#DeFiChain #DFI

"""


    return report
