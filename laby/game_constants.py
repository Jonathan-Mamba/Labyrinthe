import random
from typing import Iterable
import pygame
import icecream
import numpy as np
from typing import Any
from laby.util import laby_generator, MetaSingleton

"""
// but you played basketball right? how come you aren't perfect in any other sports??? well... whatever a sport is a sport right, they aren't that different.
LabGameConstants et LabEngineConstants contain game data.
the fist contains mostly immutable data that any part of the game can need
the second contains data that only LabGameEngine and some observers need
both classes are supposed to be singletons and their instances should be obtained through LabGameEngine or EventObserver
LOL this is outdated
LabGameConstants is now a real singleton and can be accessed anywhere
"""


class LabArray(np.ndarray):
    def get(self, index: Iterable) -> int:
        """
        returns lab_array[index[1], index[0]]
        """
        return self.__array__()[index[1], index[0]]


class LabGameConstants(metaclass=MetaSingleton):
    def __init__(self):
        # data that any part of the of game would want and shouldn't be set
        # this is not java: I won't write get methods for allat (maybe that I'll need to put a lock on this though)
        # also maybe, I said maybe there will be times when I need to change their value
        self.closed = False
        #random.seed(0)
        self.LAB_SHAPE = np.array([7, 7], dtype=np.uint16)
        self.FRAMERATE: int = 120
        self.BORDER_WIDTH = 300
        self.CELL_WIDTH = 2 * self.BORDER_WIDTH  # 600
        self.WALL_WIDTH = self.CELL_WIDTH / 6  # 120
        self.SPEED: float = 5
        self.CAMERABOX_OFFSET: int = 50
        self.SCREEN_RES = np.array([640, 480])

        self.PLAYER_SIZE = pygame.Vector2(25, 21)
        self.PLAYER_SCALE = 2

        self.labyrinth: np.ndarray[Any, int] = laby_generator.generate_lab(self.LAB_SHAPE)
        self.lab_array: LabArray = LabArray(self.LAB_SHAPE[::-1], np.int32)
        self.branch_array = np.array([0], dtype=np.int16)  # contains the indexes where a new branch start
        prev_value = np.zeros(2)
        for index, value in enumerate(self.labyrinth):
            if sum(abs(prev_value - value)) > 1:
                self.branch_array = np.append(self.branch_array, index)
            self.lab_array[value[1], value[0]] = index
            prev_value = value
        self.closed = True

    def __setattr__(self, key: str, value: Any):  # comme ça j'ai pas besoin d'écrire 50 getters
        if key == "closed":
            if value is False:
                if self.__dict__.get("closed", None) is None:  # si self.closed n'est pas présent
                    self.__dict__.update({"closed": False})
            else:
                self.__dict__.update({"closed": True})
        elif not self.closed or key in ("SCREEN_RES"):
            self.__dict__.update({key: value})


