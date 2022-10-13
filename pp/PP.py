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
    "par": "()",
}


def read_symb(node_tree):
    kind = node_tree["kind"]
    if kind in Symbols:
        return Symbols[kind]
    else:
        raise ValueError(f"Invalid kind `{kind}`")


def format_node(node_tree, direction):
    if node_tree[direction]["kind"] == "num":
        return node_tree[direction]["val"]

    elif node_tree[direction]["kind"] != "num":
        child = node_tree[direction]
        left_str = format_node(child, "left")
        right_str = format_node(child, "right")
        if read_symb(child) != "\\fract":
            return f"{left_str} {read_symb(child)} {right_str}"
        else:
            return f"{read_symb(child)}{{{left_str}}}{{{right_str}}}"


def add(node_tree):
    if node_tree["kind"] == "add":

        left = format_node(node_tree, "left")
        right = format_node(node_tree, "right")
        return f"{left} + {right}"


print(add(test))
