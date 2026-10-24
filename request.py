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

print(" ▄████████    ▄█    █▄     ▄█    ▄▄▄▄███▄▄▄▄     ▄▄▄▄███▄▄▄▄   ███    █▄     ▄████████")
print("███    ███   ███    ███   ███  ▄██▀▀▀███▀▀▀██▄ ▄██▀▀▀███▀▀▀██▄ ███    ███   ███    ███")
print("███    █▀    ███    ███   ███▌ ███   ███   ███ ███   ███   ███ ███    ███   ███    █▀")
print("███         ▄███▄▄▄▄███▄▄ ███▌ ███   ███   ███ ███   ███   ███ ███    ███   ███")
print("███        ▀▀███▀▀▀▀███▀  ███▌ ███   ███   ███ ███   ███   ███ ███    ███ ▀███████████")
print("███    █▄    ███    ███   ███  ███   ███   ███ ███   ███   ███ ███    ███          ███")
print("███    ███   ███    ███   ███  ███   ███   ███ ███   ███   ███ ███    ███    ▄█    ███")
print("████████▀    ███    █▀    █▀    ▀█   ███   █▀   ▀█   ███   █▀  ████████▀   ▄████████▀")
print("                                     ___________________ _________________ ____________")
print("                                     _  ___/  __ \_  __ `__ \__  __ \  __ `/_  ___/  _ \\")
print("                                     / /__ / /_/ /  / / / / /_  /_/ / /_/ /_  /   /  __/")
print("                                     \___/ \____//_/ /_/ /_/_  .___/\__,_/ /_/    \___/")

own_key = 0
env_on = input("Do you have a .env file with your api key (y,n) ❯ ")
if env_on == "y" or env_on == "Y" or "env_on" == "yes" or env_on == "Yes" or env_on == "YES":
    own_key = 0
elif env_on == "q" or env_on == "Q" or env_on == "QUIT" or env_on == "Quit" or env_on == "quit":
    print("exiting program")
    exit()
else:
    API_KEY = input("Please enter your API key ❯ ")
    if API_KEY == "q" or API_KEY == "Q" or API_KEY == "QUIT" or API_KEY == "quit" or API_KEY == "Quit":
        print("exiting program")
        exit()
    API_KEY = API_KEY.strip()
    own_key = 1


def _get_api_key() -> str:
    if own_key == 0:
        load_dotenv()
        key = os.getenv("MARKETSTACK_API_KEY")
        return key
    else: 
        return API_KEY



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
    user_stock = input("Enter your stock symbol(s) ❯ ").strip() # strip removes whitespace from the beginning and end of the string. just incase
    if user_stock == "quit" or user_stock == "QUIT" or user_stock == "Quit":
        exit()
    symbols = user_stock.upper().split() # splitting the symbols up
    if not symbols:
        continue

    first = symbols[0]
    try:
        data = fetch_eod_data(first, 7)
    except Exception:
        print("possible errors found: not a valid stock symbol!, refresh your api key!")
        continue
    prices = data["data"]
    prices.reverse()

    second = symbols[1] if len(symbols) > 1 else None
    if second:
        try:
            data2 = fetch_eod_data(second, 7)
        except Exception:
            print("possible errors found: not a valid stock symbol!, refresh your api key!")            
            continue
        prices2 = data2["data"]
        prices2.reverse()

    plt.clear_terminal() # clear the terminal, we use this because i'd rather use this than using the os one because i want this to be a little bit more compatible
    plt.clear_data() # clear plot data
    plt.clear_figure() # clear the plot
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
    growthper = growth1 / closes[-1] * 100
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
        label=first,
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

    if second:
        title = f"{first} vs {second}"
    else:
        title = first
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.show()
    if growthper > 0:
        print(f"{first} gained {growthper}%")
    else:
        print(f"{first} lost {growthper}%")
    if second:
        if growthper2 > 0:
            print(f"{second} gained {growthper2}%")
        else:
            print(f"{second} lost {growthper2}%")

    if second:
        if better1 > better2:
            print(f"{first}'s price rises more than {second}!")
            point1 += 1
        elif better2 > better1:
            print(f"{second}'s price rise more than {first}!")
            point2 += 1
        if better1 == better2:
            print(f"rising seems to be the same!")
            point2 += 1
            point1 += 1
    if second:
        if growthper > growthper2:
            print(f"{first} grew more than {second}!")
            point1 += 1
        elif growthper2 > growthper:
            print(f"{second} grew more than {first}!")
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
            print(f"{first} lost value by {growthper}%")
        if growthper2 < 0:
            print(f"{second} lost value by {growthper2}%")
    if second:
        if point1 > point2:
            print(f"{first} seems to be the better option")
        elif point2 > point1:
            print(f"{second} seems to be better option")
        else:
            print("Both options seem to be good options")
    # eventually we will track the percentage growth to truly track
