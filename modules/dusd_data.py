# ======================================
# DeFiChain Intelligence v4
# DUSD Data Layer
# ======================================


import requests


OCEAN_API = (
    "https://ocean.defichain.com/v0"
)



# ======================================
# DUSD Preis
# ======================================


def get_dusd_price():


    try:


        # Platzhalter:
        # echte Ocean API Anbindung folgt

        return None



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


    return None





# ======================================
# DUSD Burn
# ======================================


def get_dusd_burn():


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
