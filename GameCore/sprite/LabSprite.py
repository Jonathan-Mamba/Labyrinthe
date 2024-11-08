import typing
import numpy as np
import pygame


class LabSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def zoom_behavior(self, game_consts, y: int) -> None:
        self.image = pygame.transform.scale_by(self.image, float(game_consts.ZOOM_SCALE_STEP) * y + 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_onscreen_rect(self, offset: np.ndarray[int]) -> pygame.Rect:
        return pygame.Rect(self.rect.topleft - offset, self.rect.size)
