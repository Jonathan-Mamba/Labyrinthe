import typing
from itertools import cycle

import icecream
import numpy as np


def rel_pos(_point: np.ndarray, other: np.ndarray):
    x, y = _point - other
    if x > 0: return "left"
    if x < 0: return "right"
    if y > 0: return "up"
    if y < 0: return "down"
    return ""


if __name__ == '__main__':
    a, b, m = [
        [1, 1],
        [2, 2],
        [1, 2]
    ]
    x = np.array(a) - np.array(b)
    y = np.array(b) - np.array(m)
    icecream.ic(a)
    icecream.ic(b)
    icecream.ic(m)
    icecream.ic(x)
    icecream.ic(y)
    icecream.ic(abs(x))
    icecream.ic(x[0] * x[1])

    """
    ┌ -> y[0] > 0 && a * b < 0 #
    ┐ -> y[0] < 0 && a * b > 0
    └ -> y[0] > 0 && a * b > 0
    ┘ -> y[0] < 0 && a * b < 0
    """
