

"""
contient la classe qui représente un point du labyrinthe
"""

import abc
import numpy
import pygame
from icecream import ic
from abc import ABCMeta

from laby_generator import close_points, is_inside

type coordinate = list[int]


class ICell(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, game, index: int, pos: coordinate = [0, 0], color=[255, 255, 255], **kwds) -> None: raise NotImplementedError
    @abc.abstractmethod
    def resize(self, **kwds) -> object:...

    def __init_subclass__(cls) -> None:
        truc = [i for i in ("resize", "") if i not in cls.__dict__]
        if len(truc) > 1: 
            raise NotImplementedError(f"{cls.__name__} class does not implement {truc}")




class Cell(ICell):
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
        return [int(self.game.lab_array[*i]) for i in close_points(self.arr_index) if is_inside(i, [0, 0], self.game.LAB_SIZE)]
    
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
    
    def choose_resize_direction(self) -> str:
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
        rel_pos = self.choose_resize_direction()
        #ic(self.game.labyrinth[self.index], rel_pos, self.index)
        if rel_pos in ("left", "right"):
            self.image = pygame.Surface([self.game.CELL_WIDTH + self.game.BORDER_WIDTH, self.game.CELL_WIDTH])
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "left":    
                self.rect.move_ip(-self.game.BORDER_WIDTH, 0)
        
        elif rel_pos in ("up", "down"): 
            self.image = pygame.Surface([self.game.CELL_WIDTH, self.game.CELL_WIDTH + self.game.BORDER_WIDTH])
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "up":
                self.rect.move_ip(-self.game.BORDER_WIDTH, 0)
        self.image.fill(self.color if not kwds.get("color", 0) else kwds["color"])
        self.fixed_x = self.rect.x
        self.fixed_y = self.rect.y

if __name__ == '__main__':
    cell = Cell(1, index=0)