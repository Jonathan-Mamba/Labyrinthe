import typing
import pygame
import numpy as np
from GameCore.labGameConstants import LabGameConstants


class LabSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        raise TypeError("normalement c'est une classe abstraite ca")
        self.image, self.rect = None, None

    def zoom_behavior(self, game_consts: LabGameConstants, y: int) -> None:
        self.image = pygame.transform.smoothscale_by(self.image, float(game_consts.ZOOM_SCALE_STEP) * y + 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_image(self, spritesheet: pygame.Surface, topleft: typing.Iterable, size: typing.Iterable) -> pygame.Surface:
        image = pygame.Surface(size).convert_alpha()
        image.blit(spritesheet, topleft, (topleft[0], topleft[1], size[0], size[1]))
        return image