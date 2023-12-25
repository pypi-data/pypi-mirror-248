
import requests,json
def money_show(price,dec=0):
    price = round(float(str(price)),dec)
    return f"{price:,}"

import math
def round_decimals_up(number:float, decimals:int=2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor

def mask(string,n=-3):
    string = str(string)
    return string[:n].ljust(len(string), '*')

def fake_name():
    try:
        o = requests.get('https://api.namefake.com/').text
        return json.loads(o)['name']
    except:return 'Jewell Daniel'
