import typing

import numpy as np
import pygame
from GameCore.labGameConstants import LabGameConstants


class LabSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def zoom_behavior(self, game_consts: LabGameConstants, y: int) -> None:
        self.image = pygame.transform.scale_by(self.image, float(game_consts.ZOOM_SCALE_STEP) * y + 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_image(self,
                  spritesheet: pygame.Surface,
                  index: typing.Sequence[int],
                  size: typing.Sequence[int],
                  color: pygame.Color = pygame.Color(0, 0, 0),
                  scale_factor: float = 1,
                  ) -> pygame.Surface:
        image = pygame.Surface(size).convert_alpha()
        image.blit(spritesheet, (0, 0), (np.array(index) * np.array(size), size))
        image = pygame.transform.scale_by(image, scale_factor)
        image.set_colorkey(color)
        return image
