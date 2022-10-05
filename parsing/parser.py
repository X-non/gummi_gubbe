from typing import Dict, Iterable, Optional

from parsing.scanner import Token, TokenKind, scanner


# Grammer ish
""" 
expr := term; 
term := factor ( ("+"|"-") factor )*
factor := unary ( ("*"|"/") unary  )* 
unary := primary | '-' unary
primary := var | number | "(" expr ")";
var = ??single letter varialbe sometimes with subscript??
number = ??int or float literal??
"""


def parse(text: str):
    return Parser(scanner(text)).parse_expr()


def ast_node_base(kind: TokenKind):
    return {
        "kind": kind.to_ast_kind(),
    }


def binary_node(kind: TokenKind, left, right):
    base = ast_node_base(kind)
    return {**base, "left": left, "right": right}


def unary_node(kind: TokenKind, content):
    base = {}
    assert kind in [TokenKind.minus]
    if kind == TokenKind.minus:
        base["kind"] = "u-sub"

    return {**base, "expr": content}


def paren_node(content):
    return {"kind": "par", "expr": content}


def literal_node(token: Token):
    # TODO mabye parse the number
    return {**ast_node_base(token.kind), "val": token.lexeme}


class Parser:
    def __init__(self, tokens: Iterable[Token]):
        self.is_done = False
        self.tokens = iter(tokens)
        self.peek_token = None

    def peek(self) -> Optional[Token]:
        if self.peek_token is None:
            try:
                self.peek_token = self.tokens.__next__()
            except StopIteration:
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

        return None

    def parse_expr(self):
        return self.parse_term()

    def parse_unary(self):
        if self.eat_if(TokenKind.minus):
            return unary_node(TokenKind.minus, self.parse_unary())
        elif self.eat_if(TokenKind.open_paren):
            content = self.parse_expr()
            assert self.eat_if(TokenKind.closed_paren) is not None
            return paren_node(content)
        elif (token := self.eat_if(TokenKind.varible, TokenKind.number)) is not None:
            return literal_node(token)
        else:
            raise ValueError(f"unexpected token `{self.peek()}`")

    def parse_factor(self):
        return self.parse_binary(self.parse_unary, TokenKind.plus, TokenKind.minus)

    def parse_term(self):
        return self.parse_binary(self.parse_factor, TokenKind.plus, TokenKind.minus)

    def parse_binary(self, operand_parser, *bin_ops: TokenKind):
        working_expr = operand_parser()
        while (token := self.eat_if(*bin_ops)) is not None:
            right = operand_parser()
            working_expr = binary_node(token.kind, working_expr, right)
        return working_expr
