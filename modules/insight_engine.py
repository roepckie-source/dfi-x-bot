# ======================================
# DeFiChain Intelligence v5
# Daily Insight Engine
# ======================================


from language_manager import load_language


def generate_daily_insight(

        market,
        tokenomics,
        dusd,
        community,
        network,
        language="en"

):

    lang = load_language(language)

    insights = []



    # ==============================
    # Market Analyse
    # ==============================

    try:

        change = float(

            market
            .get("dfi", {})
            .get("change", 0)

        )


        if change >= 5:

            insights.append(

                f"🟢 Market recovery detected: DFI gained {change:.2f}% in 24h."

            )


        elif change <= -5:

            insights.append(

                f"🔴 Market pressure detected: DFI lost {abs(change):.2f}% in 24h."

            )


        else:

            insights.append(

                "🟡 Market stable with limited movement."

            )


    except:

        pass




    # ==============================
    # Tokenomics Analyse
    # ==============================


    try:


        burn = float(

            tokenomics
            .get("burn", {})
            .get("total",0)

        )


        emission = float(

            tokenomics
            .get("emission",0)

        )


        difference = burn - emission



        if difference > 0:


            insights.append(

                f"🔥 Tokenomics positive: Burn exceeds emission by {difference/1_000_000:.2f} M DFI."

            )


        else:


            insights.append(

                "⚠️ Emission currently exceeds burn."

            )



    except:

        pass




    # ==============================
    # dUSD Analyse
    # ==============================


    try:


        health = int(

            dusd
            .get(
                "health_score",
                0
            )

        )



        peg = float(

            dusd
            .get(
                "peg_difference",
                0
            )

        )



        if health < 30:


            insights.append(

                f"⚠️ dUSD remains critical: Peg deviation {peg:.2f}%."

            )


        elif health < 60:


            insights.append(

                "🟡 dUSD health improving but remains under pressure."

            )


        else:


            insights.append(

                "🟢 dUSD health stable."

            )


    except:

        pass





    # ==============================
    # Network Analyse
    # ==============================


    try:


        status = network.get(

            "network_status",

            ""

        )


        if "Online" in status:


            insights.append(

                "⛓ Network healthy: Blockchain operating normally."

            )


    except:

        pass




    # ==============================
    # Ausgabe
    # ==============================


    return "\n\n".join(

        insights

    )
