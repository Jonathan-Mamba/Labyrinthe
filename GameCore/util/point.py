import numpy as np

from gameTypes import int_coordinate

type T = int | float


class Point:
    type T = T

    def __init__(self, iterable: int_coordinate = None, x: T = None, y: T = None):
        if iterable is not None:
            self.iterable: int_coordinate = iterable
            self.x: int = self.iterable[0]
            self.y: int = self.iterable[1]
        elif type(x) not in [int, float] or type(y) in [int, float]:
            raise ValueError("Point object should contain an int or a float")
        elif (x is not None and y is not None) and (type(x) == type(y)):
            self.iterable = np.array((x, y))
            self.x, self.y = x, y
        elif type(x) != type(y):
            raise ValueError("x and y should be of the same type")
        else:
            self.iterable: int_coordinate = np.array((0, 0), dtype=np.int16)
            self.x, self.y = 0, 0

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __add__(self, other):
        return Point(x=self.x+other[0], y=self.y+other[1])

    def __r

    def __getitem__(self, item):
        return self.iterable[item]

    def __setitem__(self, key, value):
        self.iterable[key] = value
