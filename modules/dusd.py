# ======================================
# DeFiChain Intelligence v4
# DUSD Health Module
# ======================================


import requests


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
)



def get_dusd_price():

    try:

        params = {

            "ids": "defichain-dusd",

            "vs_currencies": "usd"

        }


        response = requests.get(

            COINGECKO_URL,

            params=params,

            timeout=10

        )


        data = response.json()


        price = data.get(
            "defichain-dusd",
            {}
        ).get(
            "usd"
        )


        return price



    except Exception as e:


        print(
            "DUSD Price Fehler:",
            e
        )


        return None





def calculate_health_score(price):


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





def get_dusd_health():


    price = get_dusd_price()



    if price:


        peg_difference = (

            price - 1

        )



        if abs(peg_difference) < 0.01:

            status = "🟢 Stable"


        elif abs(peg_difference) < 0.05:

            status = "🟡 Beobachten"


        else:

            status = "🔴 Stark unter Peg"



    else:


        peg_difference = "N/A"

        status = "Keine Daten"





    return {


        "price":

        f"${price:.4f}"

        if price

        else

        "N/A",



        "peg_difference":

        f"{peg_difference:.2%}"

        if isinstance(
            peg_difference,
            float
        )

        else

        "N/A",



        "status":

        status,



        "health_score":

        calculate_health_score(
            price
        ),



        "locked_dusd":

        "N/A",



        "burned_dusd":

        "N/A"


    }





# ======================================
# Compatibility Wrapper
# für main_v4_test.py
# ======================================


def get_dusd_data():

    return get_dusd_health()
