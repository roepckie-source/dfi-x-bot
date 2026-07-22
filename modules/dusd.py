# ======================================
# DeFiChain Intelligence v4
# DUSD Analyst Health Engine
# ======================================


from modules.dusd_data import get_dusd_data





# ======================================
# Peg Bewertung
# Gewicht 40 %
# ======================================


def calculate_peg_score(price):


    if not price:

        return 0



    deviation = abs(
        1 - float(price)
    )



    score = 100 - (
        deviation * 100
    )


    return max(
        0,
        round(score)
    )





# ======================================
# Locked DUSD Bewertung
# Gewicht 25 %
# ======================================


def calculate_locked_score(value):


    if value is None:

        return 50



    # wird später kalibriert

    return 50





# ======================================
# Burn Bewertung
# Gewicht 15 %
# ======================================


def calculate_burn_score(value):


    if value is None:

        return 50



    return 50





# ======================================
# Stability Fund / Community
# Gewicht 10 %
# ======================================


def calculate_stability_score():


    return 50





# ======================================
# Trend
# Gewicht 10 %
# ======================================


def calculate_trend_score():


    return 50





# ======================================
# Gesamt Health Score
# ======================================


def calculate_health_score(

        peg_score,

        locked_score,

        burn_score,

        stability_score,

        trend_score

):


    score = (

        peg_score * 0.40

        +

        locked_score * 0.25

        +

        burn_score * 0.15

        +

        stability_score * 0.10

        +

        trend_score * 0.10

    )


    return round(score)





# ======================================
# Status
# ======================================


def get_status(score):


    if score >= 80:

        return "🟢 Gesund"



    elif score >= 50:

        return "🟡 Beobachten"



    else:

        return "🔴 Kritisch"





# ======================================
# Hauptfunktion
# ======================================


def get_dusd_health():


    data = get_dusd_data()



    price = data.get(
        "price"
    )


    locked = data.get(
        "locked_dusd"
    )


    burned = data.get(
        "burned_dusd"
    )





    if price:


        peg_difference = (

            float(price) - 1

        )


    else:


        peg_difference = None





    peg_score = calculate_peg_score(
        price
    )



    locked_score = calculate_locked_score(
        locked
    )



    burn_score = calculate_burn_score(
        burned
    )



    stability_score = calculate_stability_score()



    trend_score = calculate_trend_score()





    health_score = calculate_health_score(

        peg_score,

        locked_score,

        burn_score,

        stability_score,

        trend_score

    )





    return {



        "price":

        f"${float(price):.4f}"

        if price

        else

        "N/A",



        "peg_difference":

        f"{peg_difference:.2%}"

        if peg_difference is not None

        else

        "N/A",



        "peg_score":

        peg_score,



        "locked_dusd":

        locked

        if locked

        else

        "N/A",



        "locked_score":

        locked_score,



        "burned_dusd":

        burned

        if burned

        else

        "N/A",



        "burn_score":

        burn_score,



        "stability_score":

        stability_score,



        "trend_score":

        trend_score,



        "health_score":

        health_score,



        "status":

        get_status(
            health_score
        )

    }





# ======================================
# Kompatibilität für main_v4_test.py
# ======================================


def get_dusd_data_old():

    return get_dusd_health()
