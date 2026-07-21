# ==============================
# DeFiChain Daily Intelligence v4
# Language Manager
# ==============================


from datetime import datetime
import json
import os



LANGUAGE_ORDER = [

    "en",

    "de",

    "es",

    "zh",

    "fr",

    "hi",

    "en"

]



def get_daily_language():


    day = datetime.now().weekday()


    return LANGUAGE_ORDER[day]





def load_language(language):


    path = os.path.join(

        "languages",

        f"{language}.json"

    )


    try:


        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    except Exception as e:


        print(

            "Language loading error:",

            e

        )


        return {}
