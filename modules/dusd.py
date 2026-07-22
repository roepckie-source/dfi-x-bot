# ======================================
# DeFiChain Intelligence v4
# DUSD Analyst Health Engine
# Variante B
# ======================================


import requests


# CoinGecko bleibt nur als Preis-Fallback
COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
)



# ======================================
# DUSD Preis
# ======================================


def get_dusd_price():

    try:

        # mehrere mögliche IDs testen

        ids = [
            "defichain-dusd",
            "dusd"
        ]


        for coin_id in ids:


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

                return price



        return None



    except Exception as e:


        print(
            "DUSD Preis Fehler:",
            e
        )


        return None





# ======================================
# Bewertung Peg
# Gewicht 40%
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
# später echte Datenquelle
# Gewicht 25%
# ======================================


def get_locked_dusd():


    return None





def calculate_locked_score(value):


    if not value:

        return 0


    # kommt später mit
    # echten Schwellenwerten


    return 50





# ======================================
# Burn Aktivität
# Gewicht 15%
# ======================================


def get_dusd_burn():


    return None





def calculate_burn_score(value):


    if not value:

        return 0


    return 50





# ======================================
# Stabilität
# Gewicht 10%
# ======================================


def calculate_stability_score():


    # später:
    # Stability Fund
    # Community Fund
    # DUSD Pools


    return 50





# ======================================
# Trend
# Gewicht 10%
# ======================================


def calculate_trend_score():


    # später:
    # 7 Tage Verlauf


    return 50





# ======================================
# Gesamt Score
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
