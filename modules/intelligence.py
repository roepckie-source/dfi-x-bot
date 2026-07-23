# ======================================
# DeFiChain Intelligence v5
# Intelligence Engine
# ======================================


def calculate_intelligence_score(

    market,
    tokenomics,
    dusd,
    community,
    network

):


    # ===============================
    # MARKET
    # ===============================

    market_score = 50

    try:

        change = float(
            market["dfi"]["change"]
        )

        if change > 10:
            market_score += 20

        elif change > 5:
            market_score += 10

        elif change < -10:
            market_score -= 20

        elif change < -5:
            market_score -= 10

    except:

        pass



    # ===============================
    # TOKENOMICS
    # ===============================

    tokenomics_score = 100

    try:

        burn = tokenomics["burn"]["total"]

        emission = tokenomics["emission"]

        if burn < emission:

            tokenomics_score = 40

    except:

        tokenomics_score = 50



    # ===============================
    # DUSD
    # ===============================

    dusd_score = dusd.get(
        "health_score",
        0
    )



    # ===============================
    # COMMUNITY
    # ===============================

    community_score = 70

    try:

        dfi = community["dfi"]

        if dfi > 9000000:

            community_score = 90

        elif dfi > 5000000:

            community_score = 75

        else:

            community_score = 50

    except:

        pass



    # ===============================
    # NETWORK
    # ===============================

    network_score = 100

    if network.get(
        "network_status"
    ) != "🟢 Online":

        network_score = 50



    # ===============================
    # Gesamt
    # ===============================

    total = round(

        market_score * 0.25 +

        tokenomics_score * 0.30 +

        dusd_score * 0.25 +

        community_score * 0.10 +

        network_score * 0.10

    )



    return {

        "total": total,

        "market": market_score,

        "tokenomics": tokenomics_score,

        "dusd": dusd_score,

        "community": community_score,

        "network": network_score

    }
