import pygame
import numpy as np
from labyrinthe.GameCore.labGameConstants import LabGameConstants


class LabSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.image.get_rect()

    def zoom_behavior(self, game_consts: LabGameConstants, y: int) -> None:
        self.image = pygame.transform.scale(self.image,
                                            pygame.math.Vector2(self.image.get_size()) *
                                            (1 + y * float(game_consts.ZOOM_SCALE_STEP)))
        self.rect = self.image.get_rect()
