# ==============================
# DeFiChain Daily Intelligence v4
# DUSD Health Engine
# ==============================

import requests


def calculate_health(price):

    """
    DUSD Peg Bewertung
    """


    deviation = price - 1



    if price >= 0.995:

        status = "🟢 Peg stabil"
        score = 95


    elif price >= 0.97:

        status = "🟡 leichte Abweichung"
        score = 75


    elif price >= 0.90:

        status = "🟠 unter Peg"
        score = 50


    else:

        status = "🔴 stark unter Peg"
        score = 25



    return {

        "peg_difference":
            round(deviation, 6),

        "status":
            status,

        "health_score":
            score
    }



def get_dusd_data():


    try:


        # =================================
        # Platzhalter für echte API
        # =================================

        dusd_price = None



        if dusd_price is None:


            return {


                "price":
                    "N/A",


                "peg_difference":
                    "N/A",


                "status":
                    "Keine Daten",


                "health_score":
                    0,


                "locked_dusd":
                    "N/A",


                "burned_dusd":
                    "N/A"

            }



        health = calculate_health(
            dusd_price
        )



        return {


            "price":
                round(
                    dusd_price,
                    6
                ),


            **health,


            "locked_dusd":
                "N/A",


            "burned_dusd":
                "N/A"

        }



    except Exception as e:


        print(
            "DUSD Fehler:",
            e
        )


        return {


            "price":
                "N/A",


            "peg_difference":
                "N/A",


            "status":
                "Fehler",


            "health_score":
                0,


            "locked_dusd":
                "N/A",


            "burned_dusd":
                "N/A"

        }
