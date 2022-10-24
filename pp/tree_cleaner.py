

from PP import *

test = {"kind":"add",
"left":{"expr":{"kind":"mul",
                "left":{"kind":"num", "val":"1"}, "right":{"expr":{"kind":"add",
                "left":{"kind":"num", "val":"1"}, "right":{"kind":"num", "val":"1"}}, "kind":"par"}},"kind":"par"},
"right":{"expr":{"kind":"add",
                "left":{"kind":"num", "val":"1"}, "right":{"kind":"num", "val":"1"}},"kind":"par"}}


"""Onödiga paranteser:
Efter multiplikation,
När det endast finns add och sub kvar i den "grenen" av trädet ex: 


 """





Symbols = {
    "add",
    "sub",
    "mul",
    "div",
    "par"
}

non_remove_binary_nodes = ["mul", "div"]
remove_binary_nodes = ["add", "sub"]
unary_nodes = ["par", "u-sub"]
literal_nodes = ["var", "num"]

def tree_cleaner(node):
    kind=node["kind"]

    if kind in literal_nodes:
       return node

    if kind == "par":
        return tree_cleaner(node["expr"])

    if kind in remove_binary_nodes:
        left = node["left"]
        right = node["right"]

        if left["kind"] == "par":
            left = tree_cleaner(left["expr"])
        if right["kind"] == "par":
            right = tree_cleaner(right["expr"])
        return {"kind":kind, "left":left, "right":right}

    if kind in non_remove_binary_nodes:
        left = node["left"]
        right = node["right"]
        return {"kind":kind, "left":left, "right":right}


print(format_node(tree_cleaner(test)))