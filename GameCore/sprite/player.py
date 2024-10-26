import numpy as np
import pygame
import typing
import enum
from GameCore.sprite.LabSprite import LabSprite
from GameCore.util.laby_generator import is_inside


class PlayerAnimation(enum.Enum):
    IDLE = enum.auto()
    BASE_ATTACK = enum.auto()


class Player(LabSprite):
    SPRITE_SIZE = (25, 18)
    SCALE_FACTOR = 3
    FRAMES: int = 5

    def __init__(self, screen_center: typing.Iterable[float | int], *groups: tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = self.get_image(pygame.image.load("assets/player.png"), (0, 0), Player.SPRITE_SIZE,
                                    scale_factor=Player.SCALE_FACTOR)
        self.rect = self.image.get_rect(center=screen_center)
        self.animation_count: int = 0
        self.current_animation: PlayerAnimation = PlayerAnimation.IDLE
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2()

    def update(self, *args, **kwargs):
        self.rect.topleft = (self.rect.topleft[0] + self.velocity[0], self.rect.topleft[1] + self.velocity[1])
        if self.velocity.x != 0 or self.velocity.y != 0:
            self.velocity = pygame.math.Vector2()


