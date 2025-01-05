import enum
import pygame
import numpy as np
from laby.sprite.entity import Player
from laby.sprite import Cell
from laby.game_constants import LabGameConstants


class GameState(enum.Enum):
    RUNNING = enum.auto()
    MENU = enum.auto()
    GAME_LOST = enum.auto()
    GAME_WON = enum.auto()


class LabEngineConstants:
    def __init__(self):
        # data that only LabGameEngine or event.Observers should normally want
        # this class isn't a real singleton bc it would be possible to create a valid instance outside LabGameEngine if so
        # P.S.: why is there an autocorrect on a code editor ?
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.title: str = "delalos"
        self.is_open: bool = False
        self.offset = np.array([0, 0], dtype=np.int16)
        self.max_traversal_duration = 100 # seconds
        self.state: GameState = GameState.RUNNING

        # all of these values are defined in LabGameEngine.at_startup
        self.surface: pygame.surface.Surface = None
        self.camera_rect: pygame.Rect = None
        self.start_time: int = None
        self.last_cell: Cell = None

        self.cells_group: pygame.sprite.Group = pygame.sprite.Group()
        self.wall_group: pygame.sprite.Group = pygame.sprite.Group()
        self.junction_group: pygame.sprite.Group = pygame.sprite.Group()
        self.player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.groups: list[pygame.sprite.Group] = [  # all the groups sorted by depth (drawn from first to last)
            self.cells_group,
            self.wall_group,
            self.junction_group,
            self.player_group,
        ]

    @property
    def player(self) -> Player:
        return self.player_group.sprite
