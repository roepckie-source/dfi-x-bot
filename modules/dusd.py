# ======================================
# DeFiChain Intelligence v4
# DUSD Health Module
# ======================================


from modules.stats import get_stats




def get_dusd_data():


    stats = get_stats()


    dusd = stats.get(
        "dusd",
        {}
    )


    return {


        "price":

            dusd.get(
                "price",
                "N/A"
            ),



        "peg_difference":

            dusd.get(
                "peg_difference",
                "N/A"
            ),



        "health_score":

            dusd.get(
                "health_score",
                0
            ),



        "locked_dusd":

            dusd.get(
                "locked",
                "N/A"
            ),



        "burned_dusd":

            dusd.get(
                "burned",
                "N/A"
            )

    }
