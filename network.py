# ==============================
# DeFiChain Network Data v2
# ==============================

import requests


def get_dusd_data():

    try:

        # DUSD Preis über CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": "defichain-usd",
            "vs_currencies": "usd"
        }


        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        data = response.json()


        dusd_price = data.get(
            "defichain-usd",
            {}
        ).get(
            "usd",
            0
        )


        peg_difference = dusd_price - 1


        if dusd_price >= 0.99:

            peg_status = "🟢 Peg stabil"

        elif dusd_price >= 0.90:

            peg_status = "🟡 Unter Peg"

        else:

            peg_status = "🔴 Stark unter Peg"



        return {

            "price": dusd_price,

            "peg_difference": peg_difference,

            "status": peg_status

        }


    except Exception as e:


        return {

            "price": "N/A",

            "peg_difference": "N/A",

            "status": "Fehler"

        }





def get_network_data():


    # ==========================
    # Hier bleiben deine bisherigen
    # Burn Daten
    # ==========================


    network = {

        "existing_dfi": "N/A",


        "burned_dfi": {

            "address": 158909764.56224337,

            "fee": 993026.96,

            "auction": 3538007.7617579,

            "payback": 61705058.1749106,

            "emission": 98815760.9869514,

            "total": 321435128.08025473

        },


        "locked_dusd": "N/A",

        "excess_dfi": "N/A"

    }



    # DUSD hinzufügen

    network["dusd"] = get_dusd_data()



    return network
