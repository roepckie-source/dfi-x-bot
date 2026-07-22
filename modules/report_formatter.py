# ======================================
# DeFiChain Intelligence v4
# Report Formatter
# ======================================


from datetime import datetime




# ======================================
# Zahlen Formatierung
# ======================================


def format_number(value):


    if value in [

        None,

        "None",

        "N/A",

        ""

    ]:

        return "N/A"



    try:


        value = float(value)



        if value >= 1_000_000:


            return (

                f"{value / 1_000_000:.2f} M"

            )



        elif value >= 1_000:


            return (

                f"{value / 1_000:.2f} K"

            )



        else:


            return f"{value:.2f}"



    except:


        return str(value)





# ======================================
# Prozent Formatierung
# ======================================


def format_percent(value):


    if value in [

        None,

        "None",

        "N/A"

    ]:

        return "N/A"



    try:


        value = float(value)



        if value >= 0:


            return f"🟢 +{value:.2f} %"



        else:


            return f"🔴 {value:.2f} %"



    except:


        return "N/A"





# ======================================
# Haupt Report
# ======================================


def create_report(

        market,

        tokenomics,

        dusd,

        community,

        network

):


    now = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )



    # ==============================
    # Market
    # ==============================


    dfi = market.get(
        "dfi",
        {}
    )



    report = f"""
🚀 DeFiChain Intelligence

📅 {now}

━━━━━━━━━━━━━━━━━━


💰 MARKET


💎 DFI Price

🇺🇸 ${dfi.get("usd","N/A")}

🇪🇺 €{dfi.get("eur","N/A")}



📊 24h Change

{format_percent(
    dfi.get("change")
)}



🏦 Market Cap

${format_number(
    dfi.get("market_cap")
)}



📊 Volume 24h

${format_number(
    dfi.get("volume")
)}



━━━━━━━━━━━━━━━━━━


🔥 TOKENOMICS


🔥 Total Burn

{format_number(
    tokenomics.get(
        "burn",
        {}
    ).get(
        "total"
    )
)} DFI



📈 Emission

{format_number(
    tokenomics.get(
        "emission"
    )
)} DFI



⚖️ Net Change

🟢 +{format_number(
    tokenomics.get(
        "net_change"
    )
)} DFI



Details


🏠 Address

{format_number(
    tokenomics.get(
        "burn",
        {}
    ).get(
        "address"
    )
)} DFI



↩️ Payback

{format_number(
    tokenomics.get(
        "burn",
        {}
    ).get(
        "payback"
    )
)} DFI



🔨 Auction

{format_number(
    tokenomics.get(
        "burn",
        {}
    ).get(
        "auction"
    )
)} DFI



💸 Fees

{format_number(
    tokenomics.get(
        "burn",
        {}
    ).get(
        "fees"
    )
)} DFI




━━━━━━━━━━━━━━━━━━



🪙 DUSD HEALTH


💵 Price

{dusd.get(
    "price",
    "N/A"
)}



📉 Peg

{dusd.get(
    "peg_difference",
    "N/A"
)}



❤️ Health Score

{dusd.get(
    "health_score",
    0
)}/100



🔒 Locked

{format_number(
    dusd.get(
        "locked_dusd"
    )
)} DUSD



🔥 Burned

{format_number(
    dusd.get(
        "burned_dusd"
    )
)} DUSD





━━━━━━━━━━━━━━━━━━



🏦 COMMUNITY FUND


🪙 DFI

{format_number(
    community.get(
        "dfi"
    )
)} DFI



💵 dUSD

{format_number(
    community.get(
        "dusd"
    )
)} dUSD



📈 Daily Inflow

{format_number(
    community.get(
        "daily_inflow"
    )
)} DFI



💰 Value

{format_number(
    community.get(
        "usd_value"
    )
)}






━━━━━━━━━━━━━━━━━━



⛓ NETWORK


🌐 Status

{network.get(
    "network_status",
    "N/A"
)}



🧱 Block Height

{format_number(
    network.get(
        "block_height"
    )
)}



⏱ Last Block

{network.get(
    "last_block_time",
    "N/A"
)}



🖥 Masternodes

{format_number(
    network.get(
        "masternodes"
    )
)}




━━━━━━━━━━━━━━━━━━


#DeFiChain #DFI
"""


    return report
