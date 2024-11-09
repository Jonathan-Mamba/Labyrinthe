import numpy as np
import pygame
from fractions import Fraction
from GameCore.util import laby_generator
from GameCore.sprite.player import Player

"""
// but you played basketball right? how come you aren't perfect in any other sports??? well... whatever a sport is a sport right, they aren't that different.
LabGameConstants et LabEngineConstants contain game data.
the fist contains mostly immutable data that any part of the game can need
the second contains data that only LabGameEngine and some observers need
"""


class LabGameConstants:
    def __init__(self):
        # data that any part of the of game would want and shouldn't be set
        # this is python, not java: I'm too lazy to write get methods for allat
        # also maybe, I said maybe there will be times when I need to change their value (camera_rect for example)
        self.LAB_SIZE: np.ndarray[int] = np.array([7, 7], dtype=np.uint16)
        self.labyrinth: np.ndarray[int] = laby_generator.generate_lab(self.LAB_SIZE)
        self.EXIT = self.labyrinth[-1]
        self.BORDER_WIDTH = 200
        self.CELL_WIDTH = 2 * self.BORDER_WIDTH
        self.EXIT_COLOR = pygame.color.Color((0, 255, 0))
        self.SPEED: float = 5
        self.CAMERABOX_OFFSET: int = 50
        self.SCREEN_RES = np.array([640, 480])
        self.lab_array = np.zeros((self.LAB_SIZE[1], self.LAB_SIZE[0]), dtype="int16")
        for index, value in enumerate(self.labyrinth):
            self.lab_array[value[1], value[0]] = index

    @property
    def player(self) -> Player:
        return self.player_group.sprite


class LabEngineConstants:
    def __init__(self):
        # data that only LabGameEngine or event.Observers should normally want
        # P.S.: why is there an autocorrect on a code editor ?
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.title: str = "delalos"
        self.is_open: bool = False
        self.surface: pygame.surface.Surface = pygame.Surface([10, 10])
        self.offset = np.array([0, 0], dtype=np.int16)

        self.camera_rect: pygame.Rect = None

        self.cells_group: pygame.sprite.Group = pygame.sprite.Group()
        self.player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.groups: list[pygame.sprite.Group] = [  # all the groups sorted by depth (drawn from first to last)
            self.cells_group,
            self.player_group,
        ]

    @property
    def player(self) -> Player:
        return self.player_group.sprite
