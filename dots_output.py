import base64
import imp
import io
from pydot import Edge, Dot, Node


class Uniquer:
    def __init__(self, prefix: str = "") -> None:
        self._count: int = 0
        self.prefix = prefix

    def unique(self) -> str:
        return f"{self.prefix}{self.unique_int()}"

    def unique_int(self) -> int:
        self._count += 1
        return self._count


def to_dots(ast) -> Dot:
    name_prov = Uniquer("N")
    dots_code = Dot("ast", graph_type="digraph", strict=True)
    node_to_dots(ast, name_prov.unique(), name_prov, dots_code)
    return dots_code


def write_ast_to_file(ast, file):
    to_dots(ast).write_png(file)  # type: ignore


def parse_tree_to_base64(node):

    buf = io.BytesIO(bytes(to_dots(node).create(format="png")))

    return base64.b64encode(buf.getbuffer())


def symbol_of_node(node):
    assert "kind" in node
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

    raise ValueError(f"Invalid kind `{ node['kind'] }`")


def children(node):
    match node["kind"]:
        case "add" | "sub" | "mul" | "div":
            return [node["left"], node["right"]]
        case "par" | "u-sub":
            return [node["expr"]]
        case "num" | "var":
            return []

    raise ValueError(f"Invalid node: {node}")


def node_to_dots(node, id: str, name_prov: Uniquer, dots_code: Dot):
    symbol = symbol_of_node(node)
    dots_code.add_node(Node(id, label=symbol))
    # dots_code.append(f'{id} [label="{symbol}"]')
    for child in children(node):
        child_id = name_prov.unique()
        dots_code.add_edge(Edge(id, child_id))
        node_to_dots(child, child_id, name_prov, dots_code)
