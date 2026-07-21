# ==============================
# DeFiChain Network Data v2
# ==============================

import requests



# ==============================
# DUSD Daten
# ==============================

def get_dusd_data():

    try:

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


        price = data.get(

            "defichain-usd",

            {}

        ).get(

            "usd"

        )


        # Keine Daten vorhanden

        if price is None:


            return {

                "price": "N/A",

                "peg_difference": "N/A",

                "status": "Keine Daten"

            }



        difference = price - 1



        if price >= 0.99:


            status = "🟢 Peg stabil"



        elif price >= 0.90:


            status = "🟡 Unter Peg"



        else:


            status = "🔴 Stark unter Peg"




        return {


            "price": round(

                price,

                6

            ),


            "peg_difference": round(

                difference,

                6

            ),


            "status": status


        }



    except Exception as e:


        print(

            "DUSD Fehler:",

            e

        )


        return {


            "price": "N/A",

            "peg_difference": "N/A",

            "status": "Fehler"

        }




# ==============================
# Network Daten
# ==============================

def get_network_data():


    # ==========================
    # Burn / Emission Daten
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



    # ==========================
    # DUSD hinzufügen
    # ==========================

    network["dusd"] = get_dusd_data()



    return network
