# ==============================
# DeFiChain Intelligence v5
# Blockchain Network Engine
# ==============================

import requests
from datetime import datetime



OCEAN_API = "https://ocean.defichain.com/v0"



def get_blockchain_data():


    try:


        # ==============================
        # Block Height
        # ==============================


        block_response = requests.get(

            f"{OCEAN_API}/mainnet/blocks?limit=1",

            timeout=10

        )


        block_height = None
        last_block_time = None



        if block_response.status_code == 200:


            data = block_response.json()


            if "data" in data and len(data["data"]) > 0:


                block = data["data"][0]


                block_height = block.get(
                    "height"
                )


                timestamp = block.get(
                    "time"
                )


                if timestamp:


                    last_block_time = datetime.fromtimestamp(

                        timestamp

                    ).strftime(

                        "%d.%m.%Y %H:%M"

                    )





        # ==============================
        # Masternodes
        # ==============================


        masternode_response = requests.get(

            f"{OCEAN_API}/mainnet/masternodes",

            timeout=10

        )


        masternodes = None



        if masternode_response.status_code == 200:


            masternode_data = masternode_response.json()


            if "data" in masternode_data:


                masternodes = len(

                    masternode_data["data"]

                )





        return {


            "network_status":

                "🟢 Online",



            "block_height":

                block_height
                if block_height
                else "N/A",



            "last_block_time":

                last_block_time
                if last_block_time
                else "N/A",



            "masternodes":

                masternodes
                if masternodes
                else "N/A"


        }




    except Exception as e:


        print(

            "Blockchain Fehler:",

            e

        )


        return {


            "network_status":

                "🔴 Fehler",



            "block_height":

                "N/A",



            "last_block_time":

                "N/A",



            "masternodes":

                "N/A"

        }
