# ======================================
# DeFiChain Intelligence v5
# Report Formatter
# ======================================


from datetime import datetime



def format_number(value):

    if value is None:

        return "N/A"


    if isinstance(value, float):

        if abs(value) >= 1_000_000:

            return f"{value/1_000_000:.2f} M"


        if abs(value) >= 1_000:

            return f"{value/1_000:.2f} K"


        return f"{value:.4f}"


    return str(value)





def create_report(

        market,

        tokenomics,

        dusd,

        community,

        network,

        intelligence,

        daily_insight,

        history

):


    now = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )



    score = intelligence.get(
        "total",
        "N/A"
    )


    status = intelligence.get(
        "status",
        ""
    )



    report = f"""
╔════════════════════════════════════════════╗
║    🚀 DeFiChain Intelligence               ║
║                                            ║
║   Decentralized. Independent.              ║
║   Beyond Central Control.                  ║
╚════════════════════════════════════════════╝

📅 {now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 DFI INTELLIGENCE INDEX

⭐ Score
{score}/100

{status}

📈 Market
{intelligence.get("market", "N/A")}/100

🔥 Tokenomics
{intelligence.get("tokenomics", "N/A")}/100

🪙 dUSD
{intelligence.get("dusd", "N/A")}/100

🏦 Community
{intelligence.get("community", "N/A")}/100

⛓ Network
{intelligence.get("network", "N/A")}/100

"""



    # ==========================
    # Daily Insight
    # ==========================


    report += f"""
━━━━━━━━━━━━━━━━━━

💡 DAILY INSIGHT

{daily_insight}

"""



    # ==========================
    # History
    # ==========================


    if history and isinstance(history, dict):


        report += f"""
━━━━━━━━━━━━━━━━━━

📚 DEFICHAIN HISTORY

Chapter {history.get("id","N/A")}

{history.get("title","")}

{history.get("text","")}

"""
  

    # ==========================
    # Market
    # ==========================


    dfi_market = market.get(
        "dfi",
        {}
    )


    report += f"""
━━━━━━━━━━━━━━━━━━

💰 MARKET

💎 DFI Price

🇺🇸 ${dfi_market.get("usd","N/A")} | 🇪🇺 €{dfi_market.get("eur","N/A")}


📊 24h

{dfi_market.get("change","N/A")} %


🏦 Market Cap

{format_number(
    dfi_market.get("market_cap")
)}


📊 Volume

{format_number(
    dfi_market.get("volume")
)}

"""



    # ==========================
    # Tokenomics
    # ==========================


    burn = tokenomics.get(
        "burn",
        {}
    )


    report += f"""
━━━━━━━━━━━━━━━━━━

🔥 TOKENOMICS

🔥 Burn

{format_number(
    burn.get("total")
)} DFI


📈 Emission

{format_number(
    tokenomics.get("emission")
)} DFI


⚖️ Net

{tokenomics.get("status","")}

{format_number(
    tokenomics.get("net_change")
)} DFI


🏠 Address {format_number(burn.get("address"))}

↩️ Payback {format_number(burn.get("payback"))}

🔨 Auction {format_number(burn.get("auction"))}

💸 Fees {format_number(burn.get("fees"))}

"""



    # ==========================
    # dUSD
    # ==========================


    report += f"""
━━━━━━━━━━━━━━━━━━

🪙 DUSD HEALTH

💵 Price

${dusd.get("price","N/A")}


📉 Peg

{dusd.get("peg_difference","N/A")} %


❤️ Health Score

{dusd.get("health_score","N/A")}/100


🔒 Locked

{format_number(
    dusd.get("locked")
)} DUSD


🔥 Burned

{format_number(
    dusd.get("burned")
)} DUSD

"""



    # ==========================
    # Community Fund
    # ==========================


    report += f"""
━━━━━━━━━━━━━━━━━━

🏦 COMMUNITY FUND


🪙 DFI

{format_number(
    community.get("dfi")
)} DFI


💵 dUSD

{format_number(
    community.get("dusd")
)} dUSD


📈 Inflow

{format_number(
    community.get("daily_inflow")
)} DFI


💰 Value

{community.get("usd_value","N/A")}

"""



    # ==========================
    # Network
    # ==========================


    report += f"""
━━━━━━━━━━━━━━━━━━

⛓ NETWORK


🌐 Status

{network.get("network_status","N/A")}


🧱 Block Height

{format_number(
    network.get("block_height")
)}


⏱ Last Block

{network.get("last_block_time","N/A")}


🖥 Masternodes

{format_number(
    network.get("masternodes")
)}

"""


    report += """

━━━━━━━━━━━━━━━━━━

#DeFiChain #DFI
"""


    return report.strip()
