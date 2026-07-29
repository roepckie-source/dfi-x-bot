# ======================================
# DeFiChain Intelligence v5
# Daily Insight Engine
# Multi Language Version
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

                f"🟢 {lang.get('market_recovery','Market recovery detected')}: "
                f"DFI gained {change:.2f}% in 24h."

            )



        elif change <= -5:


            insights.append(

                f"🔴 {lang.get('market_pressure','Market pressure detected')}: "
                f"DFI lost {abs(change):.2f}% in 24h."

            )



        else:


            insights.append(

                f"🟡 {lang.get('market_stable','Market stable with limited movement')}."

            )



    except Exception:


        pass





    # ==============================
    # Tokenomics Analyse
    # ==============================


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



        difference = burn - emission




        if difference > 0:



            insights.append(

                f"🔥 {lang.get('tokenomics_positive','Tokenomics positive')}: "
                f"Burn exceeds emission by "
                f"{difference/1_000_000:.2f} M DFI."

            )



        else:



            insights.append(

                f"⚠️ {lang.get('emission_high','Emission currently exceeds burn')}."

            )



    except Exception:


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

                f"⚠️ {lang.get('dusd_critical','dUSD remains critical')}: "
                f"Peg deviation {peg:.2f}%."

            )




        elif health < 60:



            insights.append(

                f"🟡 {lang.get('dusd_warning','dUSD health improving but remains under pressure')}."

            )




        else:



            insights.append(

                f"🟢 {lang.get('dusd_stable','dUSD health stable')}."

            )



    except Exception:


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

                f"⛓ {lang.get('network_health','Network healthy')}: "
                f"Blockchain operating normally."

            )



    except Exception:


        pass





    # ==============================
    # Ausgabe
    # ==============================


    return "\n\n".join(

        insights

    )
