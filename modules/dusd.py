# ======================================
# DeFiChain Intelligence v4
# DUSD Analyst Health Engine
# ======================================


import requests


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
)



# ======================================
# DUSD Preis
# ======================================


def get_dusd_price():

    try:

        possible_ids = [

            "defichain-dusd",
            "dusd"

        ]


        for coin_id in possible_ids:


            params = {

                "ids": coin_id,

                "vs_currencies": "usd"

            }


            response = requests.get(

                COINGECKO_URL,

                params=params,

                timeout=10

            )


            data = response.json()


            price = data.get(
                coin_id,
                {}
            ).get(
                "usd"
            )


            if price:


                # Schutz:
                # DUSD sollte nahe 1 USD liegen

                if 0.50 <= price <= 1.50:


                    return price


                else:


                    print(
                        "Unplausibler DUSD Preis:",
                        price
                    )



        return None



    except Exception as e:


        print(
            "DUSD Preis Fehler:",
            e
        )


        return None





# ======================================
# Peg Score
# ======================================


def calculate_peg_score(price):


    if not price:

        return 0


    deviation = abs(
        1 - price
    )


    score = 100 - (
        deviation * 100
    )


    return max(
        0,
        round(score)
    )





# ======================================
# Locked DUSD
# ======================================


def get_locked_dusd():


    # später:
    # echte DeFiChain Datenquelle

    return None





def calculate_locked_score(value):


    if value is None:

        return 50


    return 50





# ======================================
# Burn
# ======================================


def get_dusd_burn():


    # später:
    # echte Burn Daten

    return None





def calculate_burn_score(value):


    if value is None:

        return 50


    return 50





# ======================================
# Stabilität
# ======================================


def calculate_stability_score():


    return 50





# ======================================
# Trend
# ======================================


def calculate_trend_score():


    return 50





# ======================================
# Health Score
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


    price = get_dusd_price()



    if price:


        peg_difference = (

            price - 1

        )


    else:


        peg_difference = None





    peg_score = calculate_peg_score(
        price
    )



    locked = get_locked_dusd()


    burned = get_dusd_burn()



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

        f"${price:.4f}"

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
# Kompatibilität
# ======================================


def get_dusd_data():

    return get_dusd_health()
