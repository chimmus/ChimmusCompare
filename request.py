import os
from typing import Dict, Any
from urllib.parse import urlencode # formats url
import json
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv # reads .env files
from datetime import datetime
import random

BASE_URL = "http://api.marketstack.com/v1/eod"

def _get_api_key() -> str:
    load_dotenv()
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
    woof = json.dumps(resp.json(), indent=4)
    print(woof)
    return resp.json()
    
fetch_eod_data('NVDA', 30)
while True: # in a loop asks for company symbol and returns data
    meoow = input("company stock nasdaq thingy meoow ")
    print(json.dumps(fetch_eod_data(meoow, 7), indent=4))
    jimps = json.dumps(fetch_eod_data(meoow, 7), indent=4)
    data = json.loads(jimps)
    prices = data["data"]
    prices.reverse()
    print(json.dumps(prices, indent=4))
    dates = []

    for day in prices:
        print(" ", day["date"], "->", day["close"])
    dates = []                                      
    for day in prices:                                
        date_string = day["date"]                       
        cleaned = date_string.replace("Z", "")        
        date_object = datetime.fromisoformat(cleaned)  
        dates.append(date_object)   
    closes = []

    for day in prices:
        close_price = day["close"]
        closes.append(close_price)

    print("All closing prices:")
    print(*closes, sep='\n')

    print("\nMin:", min(closes))
    print("Max:", max(closes))
    print("Average:", sum(closes) / len(closes))
    plt.plot(dates, closes, marker="o")   # dot at every data point
    plt.title(f"{meoow} - Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)              # tilt date labels so they don't overlap
    plt.tight_layout()
    namechart = random.randint(1, 1000000)
    plt.savefig(f"chart_{namechart}{meoow}.png", dpi=150, bbox_inches="tight")
    