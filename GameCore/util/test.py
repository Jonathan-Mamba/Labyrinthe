import typing
from itertools import cycle
import pygame
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
    print(pygame.math.Vector2(10, 5) * 3)

    """
    ┌ -> y[0] > 0 && a * b < 0 #
    ┐ -> y[0] < 0 && a * b > 0
    └ -> y[0] > 0 && a * b > 0
    ┘ -> y[0] < 0 && a * b < 0
    """
