# ==============================
# DeFiChain Daily Intelligence v5
# Market Module
# ==============================

import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
OCEAN_DFI_URL = "https://ocean.defichain.com/v0/mainnet/prices/DFI-USD"


def get_market_data():
    market_result = {
        "price": 0.0,
        "change_24h": 0.0,
        "market_cap": 0.0,
        "volume": 0.0,
        "dfi": {"usd": 0.0, "change": 0.0},
        "bitcoin": {"change": 0.0},
        "ethereum": {"change": 0.0}
    }

    try:
        params = {
            "ids": "defichain,bitcoin,ethereum",
            "vs_currencies": "usd,eur",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }

        response = requests.get(COINGECKO_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            dfi_data = data.get("defichain", {})
            dfi_usd = dfi_data.get("usd", 0.0) or 0.0
            dfi_change = dfi_data.get("usd_24h_change", 0.0) or 0.0
            
            market_result["price"] = dfi_usd
            market_result["change_24h"] = dfi_change
            market_result["market_cap"] = dfi_data.get("usd_market_cap", 0.0) or 0.0
            market_result["volume"] = dfi_data.get("usd_24h_vol", 0.0) or 0.0
            
            market_result["dfi"] = {
                "usd": dfi_usd,
                "eur": dfi_data.get("eur", 0.0) or 0.0,
                "change": dfi_change,
                "market_cap": dfi_data.get("usd_market_cap", 0.0) or 0.0,
                "volume": dfi_data.get("usd_24h_vol", 0.0) or 0.0
            }
            
            market_result["bitcoin"] = {
                "change": data.get("bitcoin", {}).get("usd_24h_change", 0.0) or 0.0
            }
            market_result["ethereum"] = {
                "change": data.get("ethereum", {}).get("usd_24h_change", 0.0) or 0.0
            }

    except Exception as e:
        print("Market CoinGecko Fehler:", e)

    # Fallback für DFI Preis über Ocean API, falls CoinGecko 0.0 geliefert hat
    if market_result["price"] == 0.0:
        try:
            ocean_res = requests.get(OCEAN_DFI_URL, timeout=5)
            if ocean_res.status_code == 200:
                ocean_data = ocean_res.json().get("data", {})
                price_val = ocean_data.get("price", {}).get("aggregated", {}).get("amount", 0.0)
                market_result["price"] = float(price_val)
                market_result["dfi"]["usd"] = float(price_val)
        except Exception as e:
            print("Market Ocean Fallback Fehler:", e)

    return market_result
