# ======================================
# DeFiChain Intelligence v6
# Global Crypto Module
# ======================================

import requests


def get_global_crypto():

    try:

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum"
            "&vs_currencies=usd"
            "&include_24hr_change=true"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()


        btc = data.get(
            "bitcoin",
            {}
        )

        eth = data.get(
            "ethereum",
            {}
        )


        return {

            "bitcoin": {
                "price": btc.get("usd"),
                "change": btc.get("usd_24h_change")
            },

            "ethereum": {
                "price": eth.get("usd"),
                "change": eth.get("usd_24h_change")
            }

        }


    except Exception as e:

        print(
            "Global Crypto Error:",
            e
        )

        return {

            "bitcoin": {
                "price": "N/A",
                "change": "N/A"
            },

            "ethereum": {
                "price": "N/A",
                "change": "N/A"
            }

        }
