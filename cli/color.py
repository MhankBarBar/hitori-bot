from __future__ import annotations
import colorama
from abc import ABC
from colorama import Fore
from colorama.ansi import AnsiFore
colorama.init()


class ColorAbc(ABC):
    BLACK: Styling
    RED: Styling
    GREEN: Styling
    YELLOW: Styling
    BLUE: Styling
    MAGENTA: Styling
    CYAN: Styling
    WHITE: Styling
    RESET: Styling
    LIGHTBLACK_EX: Styling
    LIGHTRED_EX: Styling
    LIGHTGREEN_EX: Styling
    LIGHTYELLOW_EX: Styling
    LIGHTBLUE_EX: Styling
    LIGHTMAGENTA_EX: Styling
    LIGHTCYAN_EX: Styling
    LIGHTWHITE_EX: Styling


class Styling:
    def __init__(self, color: str) -> None:
        self.color = color

    def box_bracket(self, text: str):
        return self.color + '[' + text + self.color + ']' + Fore.RESET

    def curly_bracket(self, text: str):
        return self.color + '{' + text + self.color + '}' + Fore.RESET

    def round_bracket(self, text: str):
        return self.color + '(' + text + self.color + ')' + Fore.RESET

    def icon(self, hex: int) -> str:
        return self.text(chr(hex))

    def text(self, text: str) -> str:
        return self.color + text + Fore.RESET

    def __add__(self, text: str | Styling) -> str:
        new_text: str = text.color if isinstance(text, Styling) else text
        return self.color + new_text

    def __str__(self):
        return self.color

    def __repr__(self) -> str:
        return self.color.__repr__()


class Colors(ColorAbc, AnsiFore):
    def __init__(self) -> None:
        super().__init__()
        for i in dir(self):
            if i.isupper():
                setattr(self, i, Styling(getattr(self, i)))


Color = Colors()
