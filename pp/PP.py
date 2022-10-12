test = {
"kind": "add", 
    "left": {
    "kind": "add", 
        "left": {"kind": "num", "val": "3"}, 
        "right":{ 
        "kind": "add",
        "left": {"kind": "num", "val": "3"}, 
        "right":{"kind": "num", "val": "4"}
        }} , 
    "right": {"kind": "num", "val": "36"}
}

           
def read_val(node_tree, direction):
    if node_tree[direction]["kind"] == "num":
        print("OK")
        return node_tree[direction]["val"]
    elif node_tree[direction]["kind"] != "num":
        a = temp_list(node_tree, (direction))
        left_str = read_val(a, "left")
        right_str = read_val(a, "right")
        return f"{left_str} + {right_str}"
 
def temp_list(node_tree, direction):
        temp_list = node_tree[direction]
        return (temp_list)

def add(node_tree):
    if node_tree["kind"] == "add":
        left = read_val(node_tree, "left")
        right = read_val(node_tree, "right")
        return f"{left} + {right}"  


print(add(test))
