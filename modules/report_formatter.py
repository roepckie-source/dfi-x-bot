# ======================================
# DeFiChain Intelligence v4
# Report Formatter
# ======================================


from datetime import datetime



def format_number(value):

    try:
        value = float(value)

    except:
        return "N/A"


    if abs(value) >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f} B"


    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.2f} M"


    if abs(value) >= 1_000:
        return f"{value/1_000:.2f} K"


    return f"{value:.2f}"





def format_percent(value):

    try:
        value = float(value)

    except:
        return "N/A"


    if value >= 0:
        return f"🟢 +{value:.2f} %"

    else:
        return f"🔴 {value:.2f} %"





# ======================================
# TOKENOMICS
# ======================================


def format_tokenomics(tokenomics):


    burn = tokenomics.get(
        "burn",
        {}
    )


    total_burn = burn.get(
        "total",
        0
    )


    emission = tokenomics.get(
        "emission",
        0
    )


    balance = total_burn - emission


    if balance >= 0:

        status = (
            f"🟢 +{format_number(balance)} DFI"
        )

    else:

        status = (
            f"🔴 {format_number(balance)} DFI"
        )


    return f"""
🔥 TOKENOMICS

🔥 Total Burn
{format_number(total_burn)} DFI

📈 Emission
{format_number(emission)} DFI

⚖️ Net Change
{status}


Details

🏠 Address  {format_number(burn.get('address',0))} DFI
↩️ Payback  {format_number(burn.get('payback',0))} DFI
🔨 Auction  {format_number(burn.get('auction',0))} DFI
💸 Fees     {format_number(burn.get('fee',0))} DFI

"""





# ======================================
# DUSD HEALTH
# ======================================


def format_dusd(dusd):


    return f"""
🪙 DUSD HEALTH

💵 Price
{dusd.get('price','N/A')}

📉 Peg
{dusd.get('peg_difference','N/A')}

❤️ Health Score
{dusd.get('health_score',0)}/100

🔒 Locked
{dusd.get('locked_dusd','N/A')}

🔥 Burned
{dusd.get('burned_dusd','N/A')}

"""





# ======================================
# COMMUNITY FUND
# ======================================


def format_community(community):


    return f"""
🏦 COMMUNITY FUND

🪙 DFI
{community.get('dfi','N/A')}

💵 dUSD
{community.get('dusd','N/A')}

📈 Daily Inflow
{community.get('daily_inflow','N/A')}

💰 Value
{community.get('usd_value','N/A')}

"""





# ======================================
# NETWORK
# ======================================


def format_network(blockchain):


    return f"""
⛓ NETWORK

🌐 Status
{blockchain.get('network_status','N/A')}

🧱 Block Height
{blockchain.get('block_height','N/A')}

⏱ Last Block
{blockchain.get('last_block_time','N/A')}

🖥 Masternodes
{blockchain.get('masternodes','N/A')}

"""





# ======================================
# MAIN REPORT
# ======================================


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
🇺🇸 ${dfi.get('usd','N/A')}
🇪🇺 €{dfi.get('eur','N/A')}

📊 24h Change
{format_percent(dfi.get('change','N/A'))}

🏦 Market Cap
${format_number(dfi.get('market_cap',0))}

📊 Volume 24h
${format_number(dfi.get('volume',0))}


━━━━━━━━━━━━━━━━━━


{format_tokenomics(tokenomics)}


━━━━━━━━━━━━━━━━━━


{format_dusd(dusd)}


━━━━━━━━━━━━━━━━━━


{format_community(community)}


━━━━━━━━━━━━━━━━━━


{format_network(blockchain)}


━━━━━━━━━━━━━━━━━━


#DeFiChain #DFI
"""


    return report
