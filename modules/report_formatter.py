# ======================================
# DeFiChain Intelligence v5
# Compact Report Formatter
# ======================================


from datetime import datetime



# ======================================
# Format Helfer
# ======================================


def format_number(value):

    if value in [None, "None", "N/A", ""]:
        return "N/A"

    try:

        value = float(value)

        if value >= 1_000_000:
            return f"{value/1_000_000:.2f} M"

        if value >= 1_000:
            return f"{value/1_000:.2f} K"

        return f"{value:.2f}"

    except:

        return str(value)





def format_block(value):

    if value in [None, "None", "N/A", ""]:
        return "N/A"

    try:

        return f"{int(value):,}".replace(",", ".")

    except:

        return value





def format_percent(value):

    if value in [None, "None", "N/A"]:
        return "N/A"

    try:

        value = float(value)

        if value >= 0:
            return f"🟢 +{value:.2f} %"

        return f"🔴 {value:.2f} %"

    except:

        return "N/A"





def score_status(score):

    try:

        score = int(score)

        if score >= 80:
            return "🟢 Sehr stark"

        elif score >= 60:
            return "🟡 Stabil"

        elif score >= 40:
            return "🟠 Vorsicht"

        else:
            return "🔴 Kritisch"

    except:

        return "N/A"





# ======================================
# Report erstellen
# ======================================


def create_report(

        market,

        tokenomics,

        dusd,

        community,

        network,

        intelligence

):


    now = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )



    dfi = market.get(
        "dfi",
        {}
    )



    report = f"""🚀 DeFiChain Intelligence

📅 {now}

━━━━━━━━━━━━━━━━━━

🧠 DFI INTELLIGENCE INDEX

⭐ Score
{intelligence.get("total",0)}/100

{score_status(intelligence.get("total",0))}


📈 Market
{intelligence.get("market",0)}/100

🔥 Tokenomics
{intelligence.get("tokenomics",0)}/100

🪙 dUSD
{intelligence.get("dusd",0)}/100

🏦 Community
{intelligence.get("community",0)}/100

⛓ Network
{intelligence.get("network",0)}/100


━━━━━━━━━━━━━━━━━━

💰 MARKET

💎 DFI Price
🇺🇸 ${dfi.get("usd","N/A")} | 🇪🇺 €{dfi.get("eur","N/A")}

📊 24h
{format_percent(dfi.get("change"))}

🏦 Market Cap
${format_number(dfi.get("market_cap"))}

📊 Volume
${format_number(dfi.get("volume"))}


━━━━━━━━━━━━━━━━━━

🔥 TOKENOMICS

🔥 Burn
{format_number(tokenomics.get("burn",{}).get("total"))} DFI

📈 Emission
{format_number(tokenomics.get("emission"))} DFI

⚖️ Net
🟢 +{format_number(tokenomics.get("net_change"))} DFI


🏠 Address {format_number(tokenomics.get("burn",{}).get("address"))}

↩️ Payback {format_number(tokenomics.get("burn",{}).get("payback"))}

🔨 Auction {format_number(tokenomics.get("burn",{}).get("auction"))}

💸 Fees {format_number(tokenomics.get("burn",{}).get("fees"))}


━━━━━━━━━━━━━━━━━━

🪙 DUSD HEALTH

💵 Price
${dusd.get("price","N/A")}

📉 Peg
{dusd.get("peg_difference","N/A")} %

❤️ Health Score
{dusd.get("health_score",0)}/100

🔒 Locked
{format_number(dusd.get("locked_dusd"))} DUSD

🔥 Burned
{format_number(dusd.get("burned_dusd"))} DUSD


━━━━━━━━━━━━━━━━━━

🏦 COMMUNITY FUND

🪙 DFI
{format_number(community.get("dfi"))} DFI

💵 dUSD
{format_number(community.get("dusd"))} dUSD

📈 Inflow
{format_number(community.get("daily_inflow"))} DFI

💰 Value
{format_number(community.get("usd_value"))}


━━━━━━━━━━━━━━━━━━

⛓ NETWORK

🌐 Status
{network.get("network_status","N/A")}

🧱 Block Height
{format_block(network.get("block_height"))}

⏱ Last Block
{network.get("last_block_time","N/A")}

🖥 Masternodes
{format_block(network.get("masternodes"))}


━━━━━━━━━━━━━━━━━━

#DeFiChain #DFI
"""


    return report
