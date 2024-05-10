"""
contient la classe qui représente un point du labyrinthe
"""

import abc
import itertools

import pygame
from icecream import ic

from laby_generator import close_points, is_inside

type coordinate = list[int]


class ICell(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, game, index: int, pos: coordinate = [0, 0], color=[255, 255, 255], **kwds) -> None: ...

    @abc.abstractmethod
    def resize(self, **kwds) -> object: ...


class Cell(ICell):
    colors: itertools.cycle = itertools.cycle([
        pygame.color.Color(0, 255, 0),
        pygame.color.Color(255, 0, 0),
        pygame.color.Color(0, 0, 255),
        pygame.color.Color(228, 140, 17),
        pygame.color.Color(174, 137, 194),
        pygame.color.Color(255, 0, 255)
    ])
    current_color: pygame.color.Color = pygame.color.Color(255, 0, 255)
    colors.__next__()
    def __init__(self, game, index: int, pos: coordinate = [0, 0], color=[255, 255, 255], **kwds) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([game.CELL_WIDTH, game.CELL_WIDTH])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.game = game
        self.index = index
        self.arr_index = list(reversed(self.game.labyrinth[self.index]))
        self.fixed_x = self.rect.x
        self.fixed_y = self.rect.y

    def adjacent_indexes(self) -> list[int]:
        return [int(self.game.lab_array[*i]) for i in close_points(self.arr_index) if
                is_inside(i, [0, 0], self.game.LAB_SIZE)]

    def relative_postion(self, other) -> str:
        """
        relative postion of a cell to self (left, right, up, down)
        """
        x_distance = self.game.labyrinth[self.index][0] - other.game.labyrinth[other.index][0]
        y_distance = self.game.labyrinth[self.index][1] - other.game.labyrinth[other.index][1]
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

    def copy(self) -> ICell:
        return Cell(self.game, self.index, self.rect.topleft, self.color)

    def resize(self, **kwds: dict[bool]) -> None:
        x, y = self.rect.topleft
        rel_pos = self.get_relative_position_to_previous()
        ic(self.game.labyrinth[self.index], rel_pos)
        if rel_pos in ("left", "right"):
            self.image = pygame.Surface([self.game.CELL_WIDTH + self.game.BORDER_WIDTH, self.game.CELL_WIDTH])
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "left":
                self.rect.move_ip(-self.game.BORDER_WIDTH, 0)

        elif rel_pos in ("up", "down"):
            self.image = pygame.Surface([self.game.CELL_WIDTH, self.game.CELL_WIDTH + self.game.BORDER_WIDTH])
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "up":
                self.rect.move_ip(0, -self.game.BORDER_WIDTH)
        self.set_color()
        self.fixed_x = self.rect.x
        self.fixed_y = self.rect.y

    def set_color(self):
        previous = self.copy()
        previous.index -= 1
        lab = self.game.labyrinth
        var = lab[self.index] - lab[previous.index]
        var1 = sum(abs(var))
        ic(lab[self.index], lab[previous.index], var, var1)
        if not var1 < 2:
            Cell.current_color = Cell.colors.__next__()
        self.image.fill(Cell.current_color)



if __name__ == '__main__':
    cell = Cell(1, index=0)
