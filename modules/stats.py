# ======================================
# DeFiChain Intelligence v4
# Statistics Loader
# ======================================

import json
import os


# Pfad zur JSON-Datei
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "defichain_stats.json"
)


def get_stats():
    """
    Lädt alle DeFiChain Statistiken.
    """

    try:

        with open(
            STATS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        print(
            "Stats Fehler:",
            e
        )

        return {

            "community": {

                "dfi": "N/A",

                "dusd": "N/A",

                "daily_inflow": "N/A",

                "usd_value": "N/A"

            },

            "dusd": {

                "locked": "N/A",

                "burned": "N/A"

            },

            "network": {

                "status": "🟢 Online",

                "block_height": "N/A",

                "last_block_time": "N/A",

                "masternodes": "N/A"

            }

        }
