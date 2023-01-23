import math
from datetime import datetime
from colorama import Fore, Style
from munch import *


def Dict2Obj(d) -> DefaultMunch:
    return DefaultMunch.fromDict(d, None)


def colorize(string, color="lightgreen_ex") -> str:
    return Fore.__dict__.get(color.upper()) + string + Style.RESET_ALL


def processTime(timestamp, now) -> str:
    timestamp = datetime.fromtimestamp(timestamp)
    return (now - timestamp).total_seconds()


def h2k(num: int):
    if num == 0:
        return '0'
    size_name = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    i = int(math.floor(math.log(num, 1000)))
    p = math.pow(1000, i)
    s = round(num / p, 2)
    anu = f"{s} {size_name[i]}"
    return anu.strip()[:-2] if anu.strip().endswith('.0') else anu.strip()
