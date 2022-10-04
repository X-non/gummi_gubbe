from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable


class TokenKind(Enum):
    plus = auto
    minus = auto
    multiply = auto
    divide = auto

    open_paren = auto
    closed_paren = auto


@dataclass
class Token:
    lexeme: str
    index: int
    kind: TokenKind


def illigal_chars(text: str) -> Iterable[int]:
    """
    Yields the index of illigal chars in text
    """
    if text == "":
        return
    for i, char in enumerate(text):
        is_illigal = char.isspace() or char.isalnum() or char in "+-*/()"
        if is_illigal:
            yield i
