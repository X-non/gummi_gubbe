from PP import *

test = {
    "kind": "mul",
    "left": {"kind": "num", "val": "2"},
    "right": {
        "expr": {
            "kind": "add",
            "left": {"kind": "num", "val": "1"},
            "right": {
                "expr": {"expr": {"kind": "num", "val": "2"}, "kind": "par"},
                "kind": "par",
            },
        },
        "kind": "par",
    },
}


"""Onödiga paranteser:
Efter multiplikation,
När det endast finns add och sub kvar i den "grenen" av trädet ex: 


 """


Symbols = {"add", "sub", "mul", "div", "par"}

non_remove_binary_nodes = ["mul"]
remove_binary_nodes = ["add", "div"]
unary_nodes = ["par", "u-sub"]
literal_nodes = ["var", "num"]


def remove_paren(node):
    if node["kind"] == "par":
        return remove_paren(node["expr"])
    else:
        return node


def tree_cleaner(node):
    kind = node["kind"]

    if kind in remove_binary_nodes:
        left = node["left"]
        right = node["right"]
        if left["kind"] == "par":
            left = remove_paren(left)
        if right["kind"] == "par":
            right = remove_paren(right)

        return {"kind": kind, "left": tree_cleaner(left), "right": tree_cleaner(right)}

    if kind == "sub":
        left = node["left"]
        right = node["right"]
        if left["kind"] == "par":
            left = remove_paren(left)

        if right["kind"] == "par" and right["expr"]["kind"] in literal_nodes:
            right = remove_paren(right)

        return {"kind": kind, "left": tree_cleaner(left), "right": tree_cleaner(right)}

    if kind in non_remove_binary_nodes:
        left = node["left"]
        right = node["right"]
        return {"kind": kind, "left": tree_cleaner(left), "right": tree_cleaner(right)}

    if kind in unary_nodes:
        expr = tree_cleaner(node["expr"])
        return {"kind": kind, "expr": expr}

    return node


print(format_node(test))
print(format_node(tree_cleaner(test)))
