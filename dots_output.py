from dataclasses import dataclass
from turtle import dot

from parsing.parser import parse


class Uniquer:
    def __init__(self, prefix: str = "") -> None:
        self._count: int = 0
        self.prefix = prefix

    def unique(self) -> str:
        return f"{self.prefix}{self.unique_int()}"

    def unique_int(self) -> int:
        self._count += 1
        return self._count


def to_dots(ast):
    name_prov = Uniquer("N")
    out = []
    node_to_dots(ast, name_prov.unique(), name_prov, out)

    middle = "\n   ".join(out)
    return f"digraph AST {{\n   {middle}\n}}"


def symbol_of_node(node):
    match node["kind"]:
        case "add":
            return "+"
        case "sub":
            return "-"
        case "mul":
            return "*"
        case "div":
            return "/"
        case "par":
            return "(...)"
        case "u-sub":
            return "-"
        case "num" | "var":
            return node["val"]


def children(node):
    match node["kind"]:
        case "add" | "sub" | "mul" | "div":
            return [node["left"], node["right"]]
        case "par" | "u-sub":
            return [node["expr"]]
        case "num" | "var":
            return []

    raise ValueError(f"Invalid node: {node}")


def node_to_dots(node, id, name_prov, out):
    symbol = symbol_of_node(node)
    out.append(f'{id} [label="{symbol}"]')
    for child in children(node):
        child_id = name_prov.unique()
        out.append(f"{id} -> {child_id}")
        node_to_dots(child, child_id, name_prov, out)
