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


    balance = (

        total_burn

        -

        emission

    )


    if balance >= 0:

        status = "🟢 Deflationär"

    else:

        status = "🔴 Inflationär"



    return f"""
🔥 TOKENOMICS


🔥 Total Burn

{format_number(total_burn)} DFI


📈 Emission

{format_number(emission)} DFI


⚖️ Burn vs Emission

{status}

{format_number(balance)} DFI



Details:


🏠 Address Burn

{format_number(
    burn.get(
        'address',
        0
    )
)} DFI



💸 Fee Burn

{format_number(
    burn.get(
        'fee',
        0
    )
)} DFI



🔨 Auction Burn

{format_number(
    burn.get(
        'auction',
        0
    )
)} DFI



↩️ Payback

{format_number(
    burn.get(
        'payback',
        0
    )
)} DFI

"""





def format_dusd(dusd):


    return f"""
🪙 DUSD HEALTH


💵 Price

{dusd.get(
    'price',
    'N/A'
)}



📉 Peg Difference

{dusd.get(
    'peg_difference',
    'N/A'
)}



❤️ Health Score

{dusd.get(
    'health_score',
    0
)}/100



🔒 Locked DUSD

{dusd.get(
    'locked_dusd',
    'N/A'
)}



🔥 Burned DUSD

{dusd.get(
    'burned_dusd',
    'N/A'
)}

"""





def format_community(community):


    return f"""
🏦 COMMUNITY FUND


🪙 DFI

{community.get(
    'dfi',
    'N/A'
)}



💵 dUSD

{community.get(
    'dusd',
    'N/A'
)}



📈 Daily Inflow

{community.get(
    'daily_inflow',
    'N/A'
)}



💰 USD Value

{community.get(
    'usd_value',
    'N/A'
)}

"""





def format_network(blockchain):


    return f"""
⛓ NETWORK


🌐 Status

{blockchain.get(
    'network_status',
    'N/A'
)}



🧱 Block Height

{blockchain.get(
    'block_height',
    'N/A'
)}



⏱ Last Block

{blockchain.get(
    'last_block_time',
    'N/A'
)}



🖥 Masternodes

{blockchain.get(
    'masternodes',
    'N/A'
)}

"""





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


    # echte Market Struktur

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


🇺🇸 ${dfi.get(
    'usd',
    'N/A'
)}


🇪🇺 €{dfi.get(
    'eur',
    'N/A'
)}



📊 24h Change


{dfi.get(
    'change',
    'N/A'
)} %



🏦 Market Cap


${format_number(
    dfi.get(
        'usd_market_cap',
        dfi.get(
            'market_cap',
            0
        )
    )
)}



📊 Volume 24h


${format_number(
    dfi.get(
        'volume',
        0
    )
)}



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
