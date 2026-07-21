# ==============================
# DeFiChain Network Data v3
# ==============================

import requests



# ==============================
# DUSD Health Report
# ==============================

def get_dusd_data():

    try:

        # DUSD Daten über Ocean API
        url = (
            "https://ocean.defichain.com/v0/mainnet/poolpairs"
        )


        response = requests.get(
            url,
            timeout=10
        )


        data = response.json()


        dusd_price = None


        # Suche DUSD Pool

        if "poolPairs" in data:

            for pool in data["poolPairs"]:

                symbol = pool.get(
                    "symbol",
                    ""
                )


                if "DUSD" in symbol:

                    dusd_price = pool.get(
                        "priceRatio",
                        {}
                    ).get(
                        "ab"
                    )

                    break



        if dusd_price is None:


            return {

                "price": "N/A",

                "peg_difference": "N/A",

                "status": "Keine Daten",

                "health_score": 0,

                "locked": "N/A",

                "burned": "N/A"

            }



        dusd_price = float(
            dusd_price
        )


        deviation = dusd_price - 1



        # Peg Bewertung

        if dusd_price >= 0.99:


            status = "🟢 Peg stabil"

            score = 90



        elif dusd_price >= 0.95:


            status = "🟡 leichte Abweichung"

            score = 70



        elif dusd_price >= 0.90:


            status = "🟠 Unter Peg"

            score = 50



        else:


            status = "🔴 Stark unter Peg"

            score = 25




        return {


            "price": round(
                dusd_price,
                6
            ),


            "peg_difference": round(
                deviation,
                6
            ),


            "status": status,


            "health_score": score,


            "locked": "N/A",


            "burned": "N/A"

        }



    except Exception as e:


        print(
            "DUSD Fehler:",
            e
        )


        return {

            "price": "N/A",

            "peg_difference": "N/A",

            "status": "Fehler",

            "health_score": 0,

            "locked": "N/A",

            "burned": "N/A"

        }





# ==============================
# Network Daten
# ==============================

def get_network_data():


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



    # DUSD Health anhängen

    network["dusd"] = get_dusd_data()



    return network
