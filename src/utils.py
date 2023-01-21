from munch import *
from colorama import Fore, Style
from datetime import datetime
import math


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
    anu = "%s %s" % (s, size_name[i])
    if anu.strip().endswith('.0'):
        return anu.strip()[:-2]
    return anu.strip()
