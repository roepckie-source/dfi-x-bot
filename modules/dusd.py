# ======================================
# DeFiChain Intelligence v4
# DUSD Health Engine
# Variante B
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

        params = {

            "ids": "defichain",

            "vs_currencies": "usd"

        }


        response = requests.get(

            COINGECKO_URL,

            params=params,

            timeout=10

        )


        data = response.json()


        # Fallback:
        # DeFiChain DUSD wird später
        # durch echte Chain-Daten ersetzt

        price = data.get(
            "defichain",
            {}
        ).get(
            "usd"
        )


        return price



    except Exception as e:


        print(
            "DUSD Preis Fehler:",
            e
        )


        return None





# ======================================
# Peg Bewertung
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



    if score < 0:

        score = 0


    return round(score)





# ======================================
# Locked DUSD Bewertung
# später echte Daten
# ======================================


def calculate_locked_score():


    # Platzhalter

    # wird später aus Chain/API geholt


    return 0





# ======================================
# Burn Bewertung
# später echte Daten
# ======================================


def calculate_burn_score():


    # Platzhalter

    return 0





# ======================================
# Gesamt Health Score
# ======================================


def calculate_health_score(

        peg_score,

        locked_score,

        burn_score

):


    score = (

        peg_score * 0.50

        +

        locked_score * 0.25

        +

        burn_score * 0.15

        +

        100 * 0.10

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


        peg_score = calculate_peg_score(
            price
        )



    else:


        peg_difference = None

        peg_score = 0





    locked_score = calculate_locked_score()



    burn_score = calculate_burn_score()



    health_score = calculate_health_score(

        peg_score,

        locked_score,

        burn_score

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



        "locked_score":

        locked_score,



        "burn_score":

        burn_score,



        "health_score":

        health_score,



        "status":

        get_status(
            health_score
        ),



        "locked_dusd":

        "N/A",



        "burned_dusd":

        "N/A"


    }





# ======================================
# Kompatibilität für main_v4_test.py
# ======================================


def get_dusd_data():

    return get_dusd_health()
