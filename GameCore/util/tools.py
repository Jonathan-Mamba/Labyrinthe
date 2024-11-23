import pygame
import numpy as np
import typing
from .misc import Direction


def get_image(sprite_sheet: pygame.Surface,
              index: typing.Sequence[int],
              size: typing.Sequence[int],
              scale_factor: float = 1,
              margin: int = 1,
              color: pygame.Color = pygame.Color(0, 0, 0),
              ) -> pygame.Surface:
    image = pygame.Surface(size).convert_alpha()
    image.blit(sprite_sheet, (0, 0), (np.array(index) * np.array(size) + np.array(index) * margin, size))
    image = pygame.transform.scale_by(image, scale_factor)
    image.set_colorkey(color)
    return image


def get_relative_postion(a: typing.Iterable, b: typing.Iterable) -> Direction:
    """
    relative position of b to a
    b is in the right of a (east), b is on top of a (north), b is lower than a (south)...
    y axis goes down
    """
    x_delta = a[0] - b[0]
    y_delta = a[1] - b[1]
    if x_delta < 0:
        return Direction.EAST
    if x_delta > 0:
        return Direction.WEST
    if y_delta < 0:
        return Direction.SOUTH
    if y_delta > 0:
        return Direction.NORTH
    return Direction.NONE


def get_inverse_direction(direction: Direction | int) -> Direction:
    return Direction((direction + 4) % 8)
