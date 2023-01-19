from munch import *
from colorama import Fore, Style


def Dict2Obj(d) -> DefaultMunch:
    return DefaultMunch.fromDict(d, None)


def colorize(string, color="green") -> str:
    return Fore.__dict__.get(color.upper()) + string + Style.RESET_ALL
