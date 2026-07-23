# ======================================
# DeFiChain Intelligence v5
# Intelligence Score Engine
# ======================================


def clamp(value):

    if value < 0:
        return 0

    if value > 100:
        return 100

    return round(value)




def calculate_intelligence_score(

        market,
        tokenomics,
        dusd,
        community,
        network

):


    # ==============================
    # MARKET SCORE
    # ==============================

    market_score = 50


    try:

        change = float(
            market
            .get("dfi", {})
            .get("change", 0)
        )


        if change >= 10:
            market_score += 25

        elif change >= 5:
            market_score += 15

        elif change >= 0:
            market_score += 5

        elif change <= -10:
            market_score -= 25

        elif change <= -5:
            market_score -= 15


    except:

        pass



    market_score = clamp(
        market_score
    )



    # ==============================
    # TOKENOMICS SCORE
    # ==============================

    tokenomics_score = 50


    try:

        burn = float(
            tokenomics
            .get("burn", {})
            .get("total", 0)
        )


        emission = float(
            tokenomics
            .get("emission", 0)
        )


        if burn > emission:

            tokenomics_score = 95


        else:

            tokenomics_score = 40



    except:

        tokenomics_score = 50




    # ==============================
    # DUSD SCORE
    # ==============================

    dusd_score = int(

        dusd
        .get(
            "health_score",
            0
        )

    )


    dusd_score = clamp(
        dusd_score
    )




    # ==============================
    # COMMUNITY SCORE
    # ==============================

    community_score = 50


    try:

        dfi = float(
            community
            .get(
                "dfi",
                0
            )
        )


        if dfi >= 10000000:

            community_score = 95


        elif dfi >= 5000000:

            community_score = 75


        else:

            community_score = 50



    except:

        pass




    # ==============================
    # NETWORK SCORE
    # ==============================

    network_score = 50


    if network.get(
        "network_status"
    ) == "🟢 Online":

        network_score = 100




    # ==============================
    # Gesamt Score
    # ==============================


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




def get_score_status(score):


    if score >= 80:

        return "🟢 Sehr stark"


    elif score >= 60:

        return "🟡 Stabil"


    elif score >= 40:

        return "🟠 Vorsicht"


    else:

        return "🔴 Kritisch"
