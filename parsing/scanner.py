def contains_illigal_chars(text: str) -> bool:

    for char in text:
        is_illigal = char.isalnum or char in "+-*/()"
        if is_illigal:
            return True

    return False
