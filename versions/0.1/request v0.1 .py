import os # imports operating system so we can do commands via terminal
from typing import Dict, Any
from urllib.parse import urlencode # formats url
import json # for printing json data in a readable way
import matplotlib.pyplot as plt # for making charts
import requests # requests library for making requests to api server
from dotenv import load_dotenv # reads .env files
from datetime import datetime
import random

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
    print(woof) # then this basically like js tests, we keep this here for fun!
    return resp.json() # we return the data, so when this function is called, it can be called as a variable
    
fetch_eod_data('NVDA', 30)
# loop so we can like js keep asking it and all that
while True: # in a loop asks for company symbol and returns data
    meoow = input("company stock nasdaq thingy meoow ")
    print(json.dumps(fetch_eod_data(meoow, 7), indent=4))
    jimps = json.dumps(fetch_eod_data(meoow, 7), indent=4)
    data = json.loads(jimps)
    prices = data["data"]
    prices.reverse()
    print(json.dumps(prices, indent=4))
    dates = []

    for day in prices: # so for every 'day' in the prices like uh
        print(" ", day["date"], "->", day["close"]) # then we print the date + the closing price from the json dict
    dates = []     # new list                                 
    for day in prices:       # for every 'day' in the prices dict                         
        date_string = day["date"]                       # makes a string for the date and assigns to date
        cleaned = date_string.replace("Z", "")        # removes Z and replace with nothing
        date_object = datetime.fromisoformat(cleaned)  # formats to iso 
        dates.append(date_object)   # adds the date object thing to date list
    closes = [] # close list

    for day in prices:
        close_price = day["close"] # prints the closing price for every day
        closes.append(close_price) # adds to list

    print("All closing prices:") # prints what ever this is
    print(*closes, sep='\n') # prings the closings and all that on new line

    print("\nMin:", min(closes)) # new line , closing
    print("Max:", max(closes)) # prints the maximum closing rpice
    print("Average:", sum(closes) / len(closes)) # gives the average
    plt.plot(dates, closes, marker="o")   # dot at every data point
    plt.title(f"{meoow} - Closing Price") # names the graph
    plt.xlabel("Date") # dates on axis
    plt.ylabel("Price (USD)") # axis price
    plt.xticks(rotation=45)              # tilt date labels so they don't overlap
    plt.tight_layout() #  sets the layour
    namechart = random.randint(1, 1000000) # give unique id
    plt.savefig(f"chart_{namechart}{meoow}.png", dpi=150, bbox_inches="tight")
    # meow