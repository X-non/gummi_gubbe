test = {
    "kind": "add",
    "left": {
        "kind": "add",
        "left": {"kind": "num", "val": "3"},
        "right": {
            "kind": "div",
            "left": {"kind": "num", "val": "3"},
            "right": {"kind": "num", "val": "4"},
        },
    },
    "right": {"kind": "num", "val": "36"},
}

Symbols = {
    "add": "+",
    "sub": "-",
    "mul": "\\cdot",
    "div": "\\frac",
    "par": "()",  # Mabye remove?
}

binary_nodes = ["add", "sub", "mul", "div"]
unary_nodes = ["par", "u-sub"]
literal_nodes = ["var", "num"]


def read_symb(node_tree):
    kind = node_tree["kind"]
    if kind in Symbols:
        return Symbols[kind]
    else:
        raise ValueError(f"Invalid kind `{kind}`")


def format_node(node):
    kind = node["kind"]
    if kind in literal_nodes:
        return node["val"]

    elif kind in binary_nodes:
        left = format_node(node["left"])
        right = format_node(node["right"])
        symbol = read_symb(node)

        if symbol == "\\frac":
            return f"\\frac{{{left}}}{{{right}}}"
        else:
            return f"{left} {symbol} {right}"

    elif kind == "par":
        expr = format_node(node["expr"])
        return f"({expr})"

    elif kind == "u-sub":
        expr = format_node(node["expr"])
        return f"-{expr}"

    raise NotImplementedError(f"for `{kind}`")


print(format_node(test))
