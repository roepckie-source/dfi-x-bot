# ======================================
# DeFiChain Intelligence v5
# Language Loader
# ======================================

import json
import os


def load_language(language="de"):

    file_path = os.path.join(
        "languages",
        f"{language}.json"
    )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception as e:

        print(
            "Language Load Fehler:",
            e
        )

        return {}
