# ==============================
# DeFiChain Daily Intelligence v4
# Market Module
# ==============================

import requests


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
)


def get_market_data():

    try:

        params = {

            "ids":
            "defichain,bitcoin,ethereum",

            "vs_currencies":
            "usd,eur",

            "include_market_cap":
            "true",

            "include_24hr_vol":
            "true",

            "include_24hr_change":
            "true"

        }


        response = requests.get(

            COINGECKO_URL,

            params=params,

            timeout=10

        )


        data = response.json()



        return {


            "dfi": {

                "usd":
                data.get(
                    "defichain",
                    {}
                ).get(
                    "usd"
                ),

                "eur":
                data.get(
                    "defichain",
                    {}
                ).get(
                    "eur"
                ),

                "change":
                data.get(
                    "defichain",
                    {}
                ).get(
                    "usd_24h_change"
                ),

                "market_cap":
                data.get(
                    "defichain",
                    {}
                ).get(
                    "usd_market_cap"
                ),

                "volume":
                data.get(
                    "defichain",
                    {}
                ).get(
                    "usd_24h_vol"
                )

            },



            "bitcoin": {

                "change":
                data.get(
                    "bitcoin",
                    {}
                ).get(
                    "usd_24h_change"
                )

            },



            "ethereum": {

                "change":
                data.get(
                    "ethereum",
                    {}
                ).get(
                    "usd_24h_change"
                )

            }

        }



    except Exception as e:


        print(
            "Market Fehler:",
            e
        )


        return {


            "dfi": {},

            "bitcoin": {},

            "ethereum": {}

        }
