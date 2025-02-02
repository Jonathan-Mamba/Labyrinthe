import pygame
import numpy as np
import typing
from .misc import Direction
import json


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


def get_relative_position(a: typing.Iterable, b: typing.Iterable) -> Direction:
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


def get_inverse(direction: Direction | int) -> Direction:
    return Direction((direction + 4) % 8) if direction != 8 else Direction.NONE


def get_clockwise(direction: int | Direction, times: int) -> Direction:
    return Direction((direction + times) % 8) if direction != 8 else Direction.NONE


def get_anticlockwise(direction: Direction | int, times: int) -> Direction:
    return Direction((direction - times + 8) % 8) if direction != 8 else Direction.NONE


class MetaSingleton(type):
    _instances = {}
    # idk copied the code can't explain
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AssetsLoader(metaclass=MetaSingleton):
    def __init__(self):
        with open("assets_map.json") as f:
            self._dict: dict = json.loads(f.read())

    def get(self, str_id: str, file_type: str = "png") -> str:
        file_path = self._dict[str_id]
        if file_path is None:
            raise FileExistsError(f"{str_id} is not specified")
        elif file_path == "":
            return f"assets/{str_id.replace('.', '/')}.{file_type}"
        return "assets/" + file_path
