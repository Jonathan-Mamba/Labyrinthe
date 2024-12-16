"""
contient la classe qui représente un point du labyrinthe
"""

import abc
import typing
import itertools
import numpy as np
import pygame
from GameCore.constants import LabGameConstants
from GameCore.sprite.LabSprite import LabSprite
from GameCore.util.tools import Direction
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

    def __init__(self, cell_width: int, labyrinth: np.ndarray[int], index: int, pos: coordinate = [0, 0], color=[255, 255, 255]) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([cell_width, cell_width])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect(topleft=pos)
        self.index = index
        self.arr_index: np.ndarray[int] = labyrinth[self.index]
        # le bool indique si la cellule dans cette direction est avant self
        # juste j'ai eu besion d'un set à un moment mais plus mnt (ca marche menfou)
        self.edges: set[tuple[Direction, bool]] = set()

    def __repr__(self):
        return f"<Cell({self.arr_index} at {self.index})>"

    def copy(self, cell_width: int, lab: np.ndarray[int]) -> typing.Self:
        return Cell(cell_width, lab, self.index, self.rect.topleft, self.color)

    def get_previous(self, cell_width: int, lab: np.ndarray[int]) -> typing.Self:
        return Cell(cell_width, lab, self.index - 1, self.rect.topleft, self.color)

    def set_color(self, game_consts: LabGameConstants):  # visualizes different branches
        lab = game_consts.labyrinth
        var = lab[self.index] - lab[self.get_previous(game_consts.CELL_WIDTH, game_consts.labyrinth).index]
        if sum(abs(var)) > 1:
            Cell.current_color = Cell.colors.__next__()
        self.color = Cell.current_color
        self.image.fill(self.color)
