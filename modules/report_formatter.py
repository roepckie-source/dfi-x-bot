# ======================================
# DeFiChain Intelligence v4
# Compact Telegram Report Formatter
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





# ======================================
# Report
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



    dfi = market.get(
        "dfi",
        {}
    )



    # Net Change berechnen

    net_change = tokenomics.get(
        "net_change"
    )


    if net_change in [
        None,
        "N/A"
    ]:

        try:

            net_change = (

                float(
                    tokenomics
                    .get(
                        "burn",
                        {}
                    )
                    .get(
                        "total",
                        0
                    )
                )

                -

                float(
                    tokenomics
                    .get(
                        "emission",
                        0
                    )
                )

            )


        except:

            net_change = "N/A"




    report = f"""🚀 DeFiChain Intelligence

📅 {now}

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
🟢 +{format_number(net_change)} DFI


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

❤️ Health
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
