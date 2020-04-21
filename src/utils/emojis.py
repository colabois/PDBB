from typing import Union

NUMBERS = ["\u0030\u20e3", "\u0031\u20e3", "\u0032\u20e3", "\u0033\u20e3", "\u0034\u20e3", "\u0035\u20e3",
           "\u0036\u20e3", "\u0037\u20e3", "\u0038\u20e3", "\u0039\u20e3", "\U0001f51f"]
MINUS = "\u2796"

THUMBS_UP = "\U0001f44d"
THUMBS_DOWN = "\U0001f44e"
WHITE_CHECK_MARK = "\u2705"


def write_with_number(i: Union[int, float]):
    """
    Write number with emoji

    :Basic usage:

    >>> write_with_number(23)
    '2⃣3⃣'
    >>> write_with_number(-23)
    '➖2⃣3⃣'
    >>> write_with_number(-23.34)
    '➖2⃣3⃣.3⃣4⃣'
    >>> write_with_number(-1234567890.098)
    '➖1⃣2⃣3⃣4⃣5⃣6⃣7⃣8⃣9⃣0⃣.0⃣9⃣8⃣'

    :param i: number to write
    :return: string with emojis
    """
    s = ""
    for c in str(i):
        if c == ".":
            s += "."
        elif c == "-":
            s += MINUS
        else:
            s += NUMBERS[int(c)]
    return s
