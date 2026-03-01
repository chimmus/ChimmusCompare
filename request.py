import os
from typing import Dict, Any
from urllib.parse import urlencode # formats url

import requests
from dotenv import load_dotenv # reads .env files

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
    
    return resp.json()

while True: # in a loop asks for company symbol and returns data
    meoow = input("company stock nasdaq thingy meoow ")
    tickles = fetch_eod_data(meoow, 30)
    print(tickles)

