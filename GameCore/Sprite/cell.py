"""
contient la classe qui représente un point du labyrinthe
"""

import abc
import itertools
import numpy as np
import pygame
from labyrinthe.GameCore.labGameConstants import LabGameConstants
from labyrinthe.GameCore.Sprite.LabSprite import LabSprite

type coordinate = list[int, int]
type point = coordinate


class ICell(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, gameConsts, index: int, pos: coordinate = [0, 0], color=[255, 255, 255], **kwds) -> None: ...

    @abc.abstractmethod
    def align_to_previous(self, **kwds) -> object: ...


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


class Cell(ICell, LabSprite):
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

    def __init__(self, game_consts: LabGameConstants, index: int, pos: coordinate = [0, 0], color=[255, 255, 255],
                 **kwds) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([game_consts.CELL_WIDTH, game_consts.CELL_WIDTH])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.game_consts = game_consts
        self.index = index
        self.arr_index: list[int, int] = list(reversed(self.game_consts.labyrinth[self.index]))
        self.fixed_pos = pygame.math.Vector2(self.rect.topleft)

    def __repr__(self):
        return f"<Cell({self.arr_index} at {self.index})>"

    def adjacent_indexes(self) -> list[int]: # *i = [1, 0] -> 1, 0 (unpack)
        return [int(self.game_consts.lab_array[*i]) for i in close_points(self.arr_index) if
                is_inside(i, [0, 0], self.game_consts.LAB_SIZE)]

    def relative_postion(self, other) -> str:
        """
        relative position of a cell to self (left, right, up, down)
        """
        x_distance = self.game_consts.labyrinth[self.index][0] - other.game_consts.labyrinth[other.index][0]
        y_distance = self.game_consts.labyrinth[self.index][1] - other.game_consts.labyrinth[other.index][1]
        if x_distance > 0: return "left"
        if x_distance < 0: return "right"
        if y_distance > 0: return "up"
        if y_distance < 0: return "down"
        return ""

    def get_relative_position_to_previous(self) -> str:
        _possible_indexes = [i for i in self.adjacent_indexes() if i < self.index]
        if self.index == 0 or _possible_indexes == []:
            return ""

        _previous: Cell = self.copy()
        _previous.index = max(_possible_indexes)

        return self.relative_postion(_previous)

    def copy(self):
        return Cell(self.game_consts, self.index, self.rect.topleft, self.color)

    def get_previous(self):
        return Cell(self.game_consts, self.index - 1, self.rect.topleft, self.color)

    def align_to_previous(self, zoom_step: float = 1) -> None:
        x, y = self.rect.topleft
        rel_pos = self.get_relative_position_to_previous()
        if rel_pos in ("left", "right"):
            self.image = pygame.Surface(
                np.array([self.game_consts.CELL_WIDTH + self.game_consts.BORDER_WIDTH, self.game_consts.CELL_WIDTH]) * zoom_step)
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "left":
                self.rect.move_ip(-(self.game_consts.BORDER_WIDTH * zoom_step), 0)

        elif rel_pos in ("up", "down"):
            self.image = pygame.Surface(
                np.array([self.game_consts.CELL_WIDTH, self.game_consts.CELL_WIDTH + self.game_consts.BORDER_WIDTH]) * zoom_step)
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "up":
                self.rect.move_ip(0, -(self.game_consts.BORDER_WIDTH * zoom_step))

        self.image.fill(pygame.color.Color(0xFF, 0xFF, 0xFF))
        self.set_color()
        self.fixed_pos = pygame.math.Vector2(self.rect.topleft)

    def set_color(self):  #à mettre pour visualiser les différentes branches
        lab = self.game_consts.labyrinth
        var = lab[self.index] - lab[self.get_previous().index]
        if sum(abs(var)) > 1:
            Cell.current_color = Cell.colors.__next__()
        self.image.fill(Cell.current_color)

    def update(self, *args, **kwargs) -> None:
        self.rect.topleft = self.game_consts.offset + self.fixed_pos

    def zoom_behavior(self, game_consts: LabGameConstants, y: int) -> None:
        lab = self.game_consts.labyrinth
        if self.index == 0:
            self.image = pygame.transform.scale(self.image, pygame.math.Vector2(game_consts.zoom_scale * game_consts.CELL_WIDTH))
        else:
            # c'est à cause de cette formule compliquée que c'est pas précis
            self.image = pygame.transform.scale_by(self.image, 1 + y * float(game_consts.ZOOM_SCALE_STEP))

        self.rect = self.image.get_rect( #celle-là aussi
            topleft=(lab[self.index] * game_consts.CELL_WIDTH * float(game_consts.zoom_scale)) +
                    (lab[self.index] * game_consts.BORDER_WIDTH * float(game_consts.zoom_scale)))

        self.fixed_pos = pygame.math.Vector2(self.rect.topleft)
        self.align_to_previous(float(game_consts.zoom_scale))
