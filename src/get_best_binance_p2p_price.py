import json
import requests
import datetime
import os

url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
# https://p2p.binance.com/en/trade/all-payments
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
# "transAmount": 100,
# "payTypes": ["SEPAinstant"],
payload = {
    "fiat": "HNL",
    "page": 1,
    "rows": 5,
    "tradeType": "BUY",
    "asset": "USDT",
    "countries": [],
    "proMerchantAds": False,
    "shieldMerchantAds": False,
    "filterType": "all",
    "periods": [],
    "additionalKycVerifyFilter": 0,
    "publisherType": None,
    "classifies": ["mass", "profession", "fiat_trade"]
}


def get_best_price():
    response = requests.post(url, headers=headers, json=payload)

# Checking the response status
    if response.status_code == 200:
        data = response.json()
        # Total number of advertisements

        # List of advertisements
        ads = data.get("data", [])
        adv = ads[0].get('adv', {})
        return adv.get("price", "N/A")
    else:
        print("Hubo un Error")
        return "NaN"


if __name__ == "__main__":
    pr = get_best_price()
    ct = datetime.datetime.now()
    print(ct, ", ", pr)
    home_dir = os.path.expanduser('~')
    with open(home_dir + "/best_p2p_prices.csv", 'a') as fobj:
        fobj.write("{} , {}\n".format(ct, pr))
