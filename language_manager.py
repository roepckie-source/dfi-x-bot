# ======================================
# DeFiChain Intelligence v5
# Language Manager
# ======================================

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
    "id",
    "ja",
    "pt",
    "ru",
    "ar"

]



def get_daily_language():

    day = datetime.now().weekday()

    return LANGUAGE_ORDER[day]




def load_language(language):


    base_path = os.path.dirname(
        os.path.abspath(__file__)
    )


    path = os.path.join(

        base_path,

        "languages",

        f"{language}.json"

    )

    print("🔍 Suche Sprachdatei:", path)
    
    try:


        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    except Exception as e:


        print(

            f"⚠️ Language {language} missing - fallback English"

        )


        fallback = os.path.join(

            base_path,

            "languages",

            "en.json"

        )


        with open(

            fallback,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)
