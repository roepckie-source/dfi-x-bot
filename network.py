import requests


# ==============================
# DEFICHAIN NETWORK DATEN
# Ocean API
# ==============================


def get_network_data():

    result = {

        "existing_dfi": "N/A",
        "burned_dfi": "N/A",
        "locked_dusd": "N/A",
        "excess_dfi": "N/A"

    }


    try:

        url = (
            "https://ocean.defichain.com/"
            "v0/mainnet/stats"
        )


        response = requests.get(
            url,
            timeout=20
        )


        response.raise_for_status()


        data = response.json().get(
            "data",
            {}
        )


        result["existing_dfi"] = data.get(
            "circulatingSupply",
            "N/A"
        )


        result["burned_dfi"] = data.get(
            "burned",
            "N/A"
        )


        result["locked_dusd"] = data.get(
            "dusdLocked",
            "N/A"
        )


        result["excess_dfi"] = data.get(
            "excessDFI",
            "N/A"
        )


    except Exception as e:

        print(
            "Network Daten Fehler:",
            e
        )


    return result
