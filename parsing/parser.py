from dataclasses import dataclass
from typing import Iterable, Optional

from parsing.scanner import Token, TokenKind

# Grammer ish
""" 
expr := term; 
term := factor ( ("+"|"-") factor )*
factor := unary ( ("*"|"/") unary  )* 
unary := primary | '-' (unary)+
primary := var | number | "(" expr ")";
var = ??single letter varialbe sometimes with subscript??
number = ??int or float literal??
"""


class Parser:
    def __init__(self, tokens: Iterable[Token]):
        self.is_done = False
        self.tokens = iter(tokens)
        self.peek_token = None

    def peek(self) -> Optional[Token]:
        if self.peek_token is None:
            try:
                self.peek_token = self.tokens.__next__()
            except:
                self.is_done = True
        return self.peek_token

    def eat(self):
        token = self.peek()
        self.peek_token = None
        return token

    def eat_if(self, *matches: TokenKind) -> Optional[Token]:
        token = self.peek()
        if token is None:
            return None

        if token.kind in matches:
            self.eat()

        return token

    def parse_expr(self):
        pass

    def parse_unary(self):
        pass

    def parse_factor(self):
        pass

    def parse_term(self):
        working_expr = self.parse_factor()
        while token := self.eat_if(TokenKind.plus, TokenKind.minus):
            assert token is not None, "Should have been prechecked"
            working_expr
            self.parse_factor
