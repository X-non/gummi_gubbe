from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Iterable


@unique
class TokenKind(Enum):
    plus = auto()
    minus = auto()
    multiply = auto()
    divide = auto()

    open_paren = auto()
    closed_paren = auto()
    number = auto()
    varible = auto()

    def to_ast_kind(self) -> str:
        match self:
            case TokenKind.plus:
                return "add"
            case TokenKind.minus:
                return "sub"
            case TokenKind.multiply:
                return "mul"
            case TokenKind.divide:
                return "div"

            case TokenKind.open_paren:
                return "par"
            case TokenKind.closed_paren:
                return "par"

            case TokenKind.number:
                return "num"
            case TokenKind.varible:
                return "var"


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


def scanner(text: str) -> Iterable[Token]:
    token_i = 0
    lookup_table = {
        "(": TokenKind.open_paren,
        ")": TokenKind.closed_paren,
        "+": TokenKind.plus,
        "-": TokenKind.minus,
        "/": TokenKind.divide,
        "*": TokenKind.multiply,
    }

    while token_i < len(text):
        char = text[token_i]
        single_char_token = lookup_table.get(char)
        if single_char_token is not None:
            yield Token(char, token_i, single_char_token)
            token_i += 1
        elif char.isdigit():
            first = token_i
            token_i += 1
            while token_i < len(text) and text[token_i].isdigit():
                token_i += 1
            # TODO Add float lexing
            yield Token(text[first:token_i], first, TokenKind.number)
        elif char.isalpha():
            # TODO subscripts
            yield Token(char, token_i, TokenKind.varible)
            token_i += 1
        elif char.isspace():
            token_i += 1
        else:
            raise ValueError(f"Invalid char `{char}` in text")
