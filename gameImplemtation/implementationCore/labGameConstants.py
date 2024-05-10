import numpy as np

from GameCore.gameConstants import GameConstants
import laby_generator


class LabGameConstants(GameConstants):
    def __init__(self):
        self.LAB_SIZE: np.ndarray[int] = np.array([25, 25], dtype=np.int8)
        self.labyrinth: np.ndarray[int] = laby_generator.generate_lab(self.LAB_SIZE)
