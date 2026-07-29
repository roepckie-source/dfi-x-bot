# ==============================
# DeFiChain Intelligence v5
# Language Manager
# ==============================


import json
import os
from datetime import datetime



LANGUAGE_ORDER = [

    "de",
    "en",
    "zh",
    "ja",
    "hi",
    "id",
    "fr",
    "es",
    "pt",
    "ru",
    "ar"

]



DEFAULT_LANGUAGE = "en"



def get_daily_language():


    day = datetime.now().weekday()


    return LANGUAGE_ORDER[
        day % len(LANGUAGE_ORDER)
    ]





def load_language(language=DEFAULT_LANGUAGE):


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



    except Exception:


        print(

            f"⚠️ Language {language} missing - fallback English"

        )


        fallback = os.path.join(

            "languages",

            f"{DEFAULT_LANGUAGE}.json"

        )


        try:


            with open(

                fallback,

                "r",

                encoding="utf-8"

            ) as file:


                return json.load(file)


        except Exception as e:


            print(

                "❌ English language file missing:",

                e

            )


            return {}
