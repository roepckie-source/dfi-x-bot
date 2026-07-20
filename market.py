import requests


# ==============================
# MARKTDATEN
# CoinGecko
# ==============================


def get_market_data():

    result = {

        "dfi": {},
        "bitcoin": {},
        "ethereum": {}

    }


    try:

        url = "https://api.coingecko.com/api/v3/simple/price"


        params = {

            "ids":
            "defichain,bitcoin,ethereum",

            "vs_currencies":
            "usd,eur",

            "include_24hr_change":
            "true",

            "include_market_cap":
            "true",

            "include_24hr_vol":
            "true"

        }


        response = requests.get(
            url,
            params=params,
            timeout=20
        )


        response.raise_for_status()


        data = response.json()


        result["dfi"] = data.get(
            "defichain",
            {}
        )


        result["bitcoin"] = data.get(
            "bitcoin",
            {}
        )


        result["ethereum"] = data.get(
            "ethereum",
            {} 
        )


    except Exception as e:

        print(
            "Market Daten Fehler:",
            e
        )


    return result
