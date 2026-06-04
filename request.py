# For more documentation and annotations: https://github.com/Waverley-Christian-College/3-marketstack-api-request-chimmus/wiki/Documentation
import os # imports operating system so we can do commands via terminal
from typing import Dict, Any
from urllib.parse import urlencode # formats url
import json # for printing json data in a readable way
import plotext as plt # for making charts
import requests # requests library for making requests to api server
from dotenv import load_dotenv # reads .env files
from datetime import datetime

plt.clear_terminal()

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


def _format_plotext_date(date_string: str) -> str: # we found  this code online. it basically makes it so the date format can work (we programmed this program for windows)
    date_short = date_string[:10]
    try:
        return datetime.strptime(date_short, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError as exc:
        raise ValueError("Date Form should be: %d/%m/%Y") from exc


while True: # in a loop asks for company symbol and returns data
    point1 = 0
    point2 = 0
    meoow = input("Enter your stock symbol(s): ").strip() # strip removes whitespace from the beginning and end of the string. just incase
    symbols = meoow.upper().split() # splitting the symbols up
    if not symbols:
        continue

    ouch = symbols[0]
    data = fetch_eod_data(ouch, 7)
    prices = data["data"]
    prices.reverse()

    second = symbols[1] if len(symbols) > 1 else None
    if second:
        data2 = fetch_eod_data(second, 7)
        prices2 = data2["data"]
        prices2.reverse()

    plt.clear_terminal() # clear the terminal, we use this because i'd rather use this than using the os one because i want this to be a little bit more compatible
    plt.clear_data() # clear plot data
    plt.clear_figure() # clear the plot
    print(json.dumps(prices, indent=4))
    if second:
        print(json.dumps(prices2, indent=4))
    #defining lists
    dates = []
    closes = []
    opens = []
    highs = []
    lows = []
    for day in prices: # for every day in prices we we add the thing to the list
        dates.append(_format_plotext_date(day["date"]))
        closes.append(day["close"])
        opens.append(day["open"])
        highs.append(day["high"])
        lows.append(day["low"])
    growth1 = 0
    growth2 = 0
    if closes:
        growth1 = closes[-1] - closes[0]
    else:
        growth1 = 0
    print(growth1)
    growthper = growth1 / closes[-1] * 100
    print(growthper)
    better1 = 0
    for i in range(1, len(closes)):
        if closes[i] > closes[i - 1]:
            better1 += 1
        elif closes[i] < closes[i - 1]:
            better1 -= 1

    candle_data = { # json telling us what data will be needed
        "Open": opens,
        "High": highs,
        "Low": lows,
        "Close": closes,
    }

    plt.candlestick( # creates a candle stick graph
        dates,
        data=candle_data,
        colors=["red+", "green+"], # colours for the candle stick for stock symbol 1
        label=ouch,
    )
    if second and "prices2" in locals(): # checks if there is a second symbol
        dates2 = []
        closes2 = []
        opens2 = []
        highs2 = []
        lows2 = []
        for day in prices2: # gets the closes and all that
            dates2.append(_format_plotext_date(day["date"]))
            closes2.append(day["close"])
            opens2.append(day["open"])
            highs2.append(day["high"])
            lows2.append(day["low"])
        
        better2 = 0
        for i in range(1, len(closes2)):
            if closes2[i] > closes2[i - 1]:
                better2 += 1
            elif closes2[i] < closes2[i - 1]:
                better2 -= 1
        if closes2:
            growth2 = closes2[-1] - closes2[0]
        else:
            growth2 = 0
        growthper2 = growth2 / closes2[-1] * 100
        candle_data2 = {
            "Open": opens2,
            "High": highs2,
            "Low": lows2,
            "Close": closes2,
        }
        plt.candlestick( # adds it to the graph
            dates2,
            data=candle_data2,
            colors=["blue+", "orange+"], # colours for symbol 2
            label=second,
        )

    if growthper > 0:
        print(f"{ouch} gained {growthper}%")
    else:
        print(f"{ouch} lost {growthper}%")
    if second:
        if growthper2 > 0:
            print(f"{second} gained {growthper2}%")
        else:
            print(f"{second} lost {growthper2}%")
    if second:
        title = f"{ouch} vs {second}"
    else:
        title = ouch
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.show()
    if second:
        if better1 > better2:
            print(f"{ouch}'s price rises more than {second}!")
            point1 += 1
        elif better2 > better1:
            print(f"{second}'s price rise more than {ouch}!")
            point2 += 1
        if better1 == better2:
            print(f"rising seems to be the same!")
            point2 += 1
            point1 += 1
    if second:
        if growthper > growthper2:
            print(f"{ouch} grew more than {second}!")
            point1 += 1
        elif growthper2 > growthper:
            print(f"{second} grew more than {ouch}!")
            point2 += 1
        if growthper == growthper2:
            print(f"growth seems to be the same!")
            point1 += 1
            point2 += 1
    if second:
        if growth1 > growth2:
            point1 += 1
        if growth1 < growth2:
            point2 += 1
        if growth1 == growth2:
            point1 += 1
            point2 += 1
    if second:
        if growthper < 0:
            print(f"{ouch} lost value by {growthper}%")
        if growthper2 < 0:
            print(f"{second} lost value by {growthper2}%")
    if second:
        if point1 > point2:
            print(f"{ouch} seems to be the better option")
        elif point2 > point1:
            print(f"{second} seems to be better option")
        else:
            print("Both options seem to be good options")
    # eventually we will track the percentage growth to truly track
