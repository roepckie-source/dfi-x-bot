from datetime import datetime


def get_daily_language():

    languages = [
        "en",
        "de",
        "es",
        "zh",
        "fr",
        "hi",
        "en"
    ]


    day = datetime.now().weekday()


    return languages[day]
