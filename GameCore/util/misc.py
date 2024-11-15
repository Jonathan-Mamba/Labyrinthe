import enum
import pygame
import numpy as np

type int_pos = list[int] | tuple[int, int] | np.ndarray[int]
type float_pos = pygame.math.Vector2 | list[float] | tuple[int, int] | np.ndarray[float]

class Direction(enum.IntEnum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    NONE = 8