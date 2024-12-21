"""
contient la classe qui représente un point du labyrinthe
"""

import typing
import itertools
import numpy as np
import pygame
from laby.game_constants import LabGameConstants
from laby.sprite.LabSprite import LabSprite
from laby.util.tools import Direction
type coordinate = typing.SupportsIndex[int]
type point = coordinate


def close_points(_point: point) -> list[list[int]]:
    x, y = _point[0], _point[1]
    return [
        [x - 1, y],
        [x + 1, y],
        [x, y + 1],
        [x, y - 1],
    ]


def is_inside(_point: point, topleft: point, bottomright: point) -> bool:
    return topleft[0] <= _point[0] < bottomright[0] and topleft[1] <= _point[1] < bottomright[1]


class Cell(LabSprite):
    colors: itertools.cycle = itertools.cycle([
        pygame.color.Color(0, 255, 0),
        pygame.color.Color(255, 0, 0),
        pygame.color.Color(0, 0, 255),
        pygame.color.Color(228, 140, 17),
        pygame.color.Color(174, 137, 194),
        pygame.color.Color(255, 0, 255),
        pygame.color.Color(20, 159, 35),
        pygame.color.Color(159, 20, 43)
    ])
    current_color: pygame.color.Color = pygame.color.Color(255, 0, 255)
    colors.__next__()

    def __init__(self, index: int, pos: coordinate = [0, 0], color=[255, 255, 255]) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([LabGameConstants().CELL_WIDTH, LabGameConstants().CELL_WIDTH])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect(topleft=pos)
        self.index = index
        self.arr_index: np.ndarray[int] = LabGameConstants().labyrinth[self.index]
        # le bool indique si la cellule dans cette direction est avant self
        # juste j'ai eu besion d'un set à un moment mais plus mnt (ca marche menfou)
        self.edges: set[tuple[Direction, bool]] = set()

    def __repr__(self):
        return f"<Cell({self.index} at {self.arr_index})>"

    def copy(self) -> typing.Self:
        return Cell(self.index, self.rect.topleft, self.color)

    def get_previous(self) -> typing.Self:
        return Cell(self.index - 1, self.rect.topleft, self.color)

    def set_color(self):  # visualizes different branches
        var = LabGameConstants().labyrinth[self.index] - LabGameConstants().labyrinth[self.get_previous().index]
        if sum(abs(var)) > 1:
            Cell.current_color = Cell.colors.__next__()
        self.color = Cell.current_color
        self.image.fill(self.color)
