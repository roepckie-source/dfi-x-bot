# ======================================
# DeFiChain Intelligence v4
# Network Module
# ======================================


from modules.stats import get_stats




def get_network_data():


    stats = get_stats()


    network = stats.get(
        "network",
        {}
    )



    return {


        "network_status":

        network.get(
            "status",
            "N/A"
        ),



        "block_height":

        network.get(
            "block_height",
            "N/A"
        ),



        "last_block_time":

        network.get(
            "last_block_time",
            "N/A"
        ),



        "masternodes":

        network.get(
            "masternodes",
            "N/A"
        )

    }
