# ======================================
# DeFiChain Intelligence v4
# DUSD Data Layer
# ======================================


import requests


# DeFiChain Ocean API Basis
OCEAN_API = (
    "https://ocean.defichain.com/v0"
)



# ======================================
# DUSD Marktpreis
# ======================================


def get_dusd_price():


    try:


        url = (

            OCEAN_API +

            "/prices/dusd-usd"

        )


        response = requests.get(

            url,

            timeout=10

        )


        data = response.json()


        price = data.get(
            "price"
        )


        return price



    except Exception as e:


        print(
            "DUSD Price Fehler:",
            e
        )


        return None





# ======================================
# Locked DUSD
# ======================================


def get_locked_dusd():


    try:


        # Vorbereitung für
        # echte Chain Daten


        return None



    except Exception as e:


        print(
            "Locked DUSD Fehler:",
            e
        )


        return None





# ======================================
# DUSD Burn
# ======================================


def get_dusd_burn():


    try:


        # Vorbereitung für
        # Burn Daten


        return None



    except Exception as e:


        print(
            "DUSD Burn Fehler:",
            e
        )


        return None





# ======================================
# Gesamtdaten
# ======================================


def get_dusd_data():


    return {


        "price":

        get_dusd_price(),


        "locked_dusd":

        get_locked_dusd(),


        "burned_dusd":

        get_dusd_burn()

    }
