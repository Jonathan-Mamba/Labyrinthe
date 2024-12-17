import typing
import numpy as np
import pygame


class LabSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def get_onscreen_rect(self, offset: np.ndarray[int]) -> pygame.Rect:
        return pygame.Rect(self.rect.topleft - offset, self.rect.size)
