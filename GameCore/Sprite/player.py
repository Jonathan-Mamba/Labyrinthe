import numpy as np
import pygame.image
import typing
from LabSprite import LabSprite

class Player(LabSprite):
    def __init__(self, *groups: tuple[pygame.sprite.Group], screen_center: typing.Iterable[float | int]):
        super().__init__(*groups)
        self.image = self.get_image(pygame.image.load("../../assets/player.png"), (0, 0), (25, 18))
        self.rect = self.image.get_rect(center=screen_center)
