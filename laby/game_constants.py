import pygame
import numpy as np
from laby.util import laby_generator, MetaSingleton

"""
// but you played basketball right? how come you aren't perfect in any other sports??? well... whatever a sport is a sport right, they aren't that different.
LabGameConstants et LabEngineConstants contain game data.
the fist contains mostly immutable data that any part of the game can need
the second contains data that only LabGameEngine and some observers need
both classes are supposed to be singletons and their instances should be obtained through LabGameEngine or EventObserver
"""


def __get__():
    return LabGameConstants


class LabGameConstants(metaclass=MetaSingleton):
    def __init__(self):
        # data that any part of the of game would want and shouldn't be set
        # this is not java: I won't write get methods for allat (maybe that I'll need to put a lock on this though)
        # also maybe, I said maybe there will be times when I need to change their value
        self.LAB_SHAPE: np.ndarray[int] = np.array([7, 7], dtype=np.uint16)
        self.FRAMERATE: int = 120
        self.BORDER_WIDTH = 50
        self.CELL_WIDTH = 2 * self.BORDER_WIDTH  # 600
        self.WALL_WIDTH = self.CELL_WIDTH / 6  # 120
        self.SPEED: float = 5
        self.CAMERABOX_OFFSET: int = 50
        self.SCREEN_RES = np.array([640, 480])

        self.labyrinth: np.ndarray[int] = laby_generator.generate_lab(self.LAB_SHAPE)
        self.lab_array = np.zeros((self.LAB_SHAPE[1], self.LAB_SHAPE[0]), dtype="int16")
        self.branch_array = np.array([0], dtype=np.int16)  # contains the indexes where a new branch start
        prev_value = np.zeros(2)
        for index, value in enumerate(self.labyrinth):
            if sum(abs(prev_value - value)) > 1:
                self.branch_array = np.append(self.branch_array, index)
            self.lab_array[value[1], value[0]] = index
            prev_value = value



