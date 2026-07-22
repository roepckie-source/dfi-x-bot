# ======================================
# DeFiChain Intelligence v4
# Community Fund Module
# ======================================


from modules.stats import get_stats




def get_community_data():


    stats = get_stats()


    community = stats.get(
        "community",
        {}
    )



    return {


        "dfi":

        community.get(
            "dfi",
            "N/A"
        ),



        "dusd":

        community.get(
            "dusd",
            "N/A"
        ),



        "daily_inflow":

        community.get(
            "daily_inflow",
            "N/A"
        ),



        "usd_value":

        community.get(
            "usd_value",
            "N/A"
        )

    }
