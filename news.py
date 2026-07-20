import json
from datetime import datetime


# ==============================
# DFI NEWS
# ==============================


def get_dfi_news():

    try:

        with open(
            "dfi_news.json",
            "r",
            encoding="utf-8"
        ) as file:

            news = json.load(file)


        if not news:

            return {

                "title":
                "DeFiChain Daily",

                "text":
                "No news available",

                "hashtags":
                "#DeFiChain #DFI"

            }


        day = datetime.now().timetuple().tm_yday


        index = (
            day - 1
        ) % len(news)


        return news[index]


    except Exception as e:

        print(
            "News Fehler:",
            e
        )


        return {

            "title":
            "DeFiChain Update",

            "text":
            "Daily DeFiChain Report",

            "hashtags":
            "#DeFiChain #DFI"

        }
