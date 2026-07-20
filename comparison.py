# ==============================
# MARKET COMPARISON
# DFI vs BTC vs ETH
# ==============================


def get_comparison(market):


    result = {

        "dfi_change": 0,
        "btc_change": 0,
        "eth_change": 0,
        "vs_btc": "",
        "vs_eth": ""

    }


    try:

        dfi_change = market["dfi"].get(
            "usd_24h_change",
            0
        )

        btc_change = market["bitcoin"].get(
            "usd_24h_change",
            0
        )

        eth_change = market["ethereum"].get(
            "usd_24h_change",
            0
        )


        result["dfi_change"] = dfi_change
        result["btc_change"] = btc_change
        result["eth_change"] = eth_change


        if dfi_change >= btc_change:

            result["vs_btc"] = (
                "🟢 Outperforming Bitcoin"
            )

        else:

            result["vs_btc"] = (
                "🔴 Underperforming Bitcoin"
            )



        if dfi_change >= eth_change:

            result["vs_eth"] = (
                "🟢 Outperforming Ethereum"
            )

        else:

            result["vs_eth"] = (
                "🔴 Underperforming Ethereum"
            )


    except Exception as e:

        print(
            "Comparison Fehler:",
            e
        )


    return result
