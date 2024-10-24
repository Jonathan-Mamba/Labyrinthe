import numpy as np
import pygame
from fractions import Fraction
from labyrinthe.GameCore.util import laby_generator



class LabGameConstants:
    def __init__(self):
        self.LAB_SIZE: np.ndarray[int] = np.array([25, 25], dtype=np.uint16)
        self.labyrinth: np.ndarray[int] = laby_generator.generate_lab(self.LAB_SIZE)
        self.EXIT = self.labyrinth[-1]
        self.BORDER_WIDTH = 8
        self.CELL_WIDTH = 4 * self.BORDER_WIDTH
        self.EXIT_COLOR = pygame.color.Color((0, 255, 0))
        self.OFFSET_STEP: int = 1
        self.ZOOM_SCALE_STEP: Fraction = Fraction(1, 2)

        self.cells_group: pygame.sprite.Group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()

        self.lab_array = np.zeros((self.LAB_SIZE[1], self.LAB_SIZE[0]), dtype="int16")
        for index, value in enumerate(self.labyrinth):
            self.lab_array[value[1], value[0]] = index

        self.groups: list[pygame.sprite.Group] = [
            #self.player_group,
            self.cells_group]

        self.zoom_scale: Fraction = Fraction(1, 1)
        self.screen_res: np.ndarray[int, int] = np.array([640, 480], dtype=np.int16)
        self.title: str = "delalos"
        self.is_open: bool = False
        self.surface: pygame.surface.Surface = pygame.Surface([10, 10])
        self.offset = np.array([0, 0], dtype=np.int16)
        self.pressed_keys: dict[int, bool] = {}
