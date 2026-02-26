import os
from typing import Dict, Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

BASE_URL = "http://api.marketstack.com/v1/eod"


def _get_api_key() -> str:
    load_dotenv()
    key = os.getenv("MARKETSTACK_API_KEY")
    return key


def fetch_eod_data(symbol: str, limit: int = 30) -> Dict[str, Any]:
    """
    Fetch recent EOD data for the given symbol.
    Returns dict like: {"data": [...], "pagination": {...}}
    Raises RuntimeError with a helpful message on failure.
    """
    params = {
        "access_key": _get_api_key(),
        "symbols": symbol,
        "limit": limit
    }
    url = f"{BASE_URL}?{urlencode(params)}"

    resp = requests.get(url)

    if resp.status_code != 200:
        raise RuntimeError(f"HTTP error {resp.status_code}: {resp.text[:200]}")
    
    return resp.json()
