from typing import Iterable


def illigal_chars(text: str) -> Iterable[int]:
    """
    Yields the index of illigal chars in text
    """
    if text == "":
        return
    for i, char in enumerate(text):
        is_illigal = char.isspace() or char.isalnum() or char in "+-*/()"
        if is_illigal:
            yield i
