import os # imports operating system so we can do commands via terminal
from typing import Dict, Any
from urllib.parse import urlencode # formats url
import json # for printing json data in a readable way
import plotext as plt # for making charts
import requests # requests library for making requests to api server
from dotenv import load_dotenv # reads .env files
from datetime import datetime

BASE_URL = "http://api.marketstack.com/v1/eod"

def _get_api_key() -> str: # specifies it will be a string
    load_dotenv() # loads dotenv from library
    key = os.getenv("MARKETSTACK_API_KEY") # gets api key from .env
    return key # returns the key when it is run so can be assigned to variable value


def fetch_eod_data(symbol: str, limit: int = 30) -> Dict[str, Any]:
    """
    Fetch recent EOD data for the given symbol.
    Returns dict like: {"data": [...], "pagination": {...}}
    Raises RuntimeError with a helpful message on failure.
    """
    params = { # parameters read by urlencode
        "access_key": _get_api_key(),
        "symbols": symbol,
        "limit": limit # request rate limit
    }
    url = f"{BASE_URL}?{urlencode(params)}"

    resp = requests.get(url) # gets the response

    if resp.status_code != 200: # checks if response is valid
        raise RuntimeError(f"HTTP error {resp.status_code}: {resp.text[:200]}")
    woof = json.dumps(resp.json(), indent=4) # we basically made this for like yk testing
    return resp.json() # we return the data, so when this function is called, it can be called as a variable
    
fetch_eod_data('NVDA', 30)
# loop so we can like js keep asking it and all that
while True: # in a loop asks for company symbol and returns data
    meoow = input("company stock nasdaq thingy meoow ")
    ouch = str(meoow[0] + meoow[1] + meoow[2] + meoow[3])
    print(json.dumps(fetch_eod_data(ouch, 7), indent=4))
    jimps = json.dumps(fetch_eod_data(ouch, 7), indent=4)
    data = json.loads(jimps)
    prices = data["data"]
    prices.reverse()
    print(json.dumps(prices, indent=4))
    dates = []
    if len(meoow) >= 5:
        if meoow[4] == ' ':
            if meoow[5] != ' ':
                if meoow[5] != '':
                    second = str(meoow[5] + meoow[6] + meoow[7] + meoow[8])
                    chimps = (json.dumps(fetch_eod_data(second, 7), indent=4))
                    data2 = json.loads(chimps)
                    prices2 = data2["data"]
                    prices2.reverse()
                    for day in prices2:
                        print(" ", day["date"], "->", day["close"]) 
                    dates2 = []
                    for day in prices2:
                        date_string = day["date"]
                        dates2.append(date_string[:10])
                    closes2 = []
                    for day in prices2:
                        close_price = day["close"]
                        closes2.append(close_price)

    for day in prices: # so for every 'day' in the prices like uh
        print(" ", day["date"], "->", day["close"]) # then we print the date + the closing price from the json dict
    dates = []     # new list                                 
    for day in prices:       # for every 'day' in the prices dict                         
        date_string = day["date"]                       # makes a string for the date and assigns to date
        dates.append(date_string[:10])   # adds the date string to date list
    closes = [] # close list

    for day in prices:
        close_price = day["close"] # prints the closing price for every day
        closes.append(close_price) # adds to list

    print("All closing prices:") # prints what ever this is
    print(*closes, sep='\n') # prings the closings and all that on new line

    print("\nMin:", min(closes)) # new line , closing
    print("Max:", max(closes)) # prints the maximum closing rpice
    print("Average:", sum(closes) / len(closes)) # gives the average
    
    dates_formatted = [datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y") for d in dates]
    plt.plot(dates_formatted, closes, marker="o")   # dot at every data point
    if 'dates2' in locals() and 'closes2' in locals():
        dates2_formatted = [datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y") for d in dates2]
        plt.plot(dates2_formatted, closes2, marker="s")   # dot at every data point for second stock
    plt.title(f"{ouch}") # names the graph
    plt.xlabel("Date") # dates on axis
    plt.ylabel("Price (USD)") # axis price
    plt.show()