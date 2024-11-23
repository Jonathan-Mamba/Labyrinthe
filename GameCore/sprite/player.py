import numpy as np
import pygame
import typing
import enum
from GameCore.sprite.LabSprite import LabSprite
from GameCore.util import tools


class PlayerAnimation(enum.Enum):
    IDLE = enum.auto()
    BASE_ATTACK = enum.auto()


class Player(LabSprite):
    SPRITE_SIZE = (25, 21)
    SCALE_FACTOR = 3

    def __init__(self, screen_center: typing.Iterable[float | int], *groups: tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = tools.get_image(pygame.image.load("assets/player/idle.png"), (0, 0), Player.SPRITE_SIZE,
                                     Player.SCALE_FACTOR)
        self.rect = self.image.get_rect(center=screen_center)
        self.animation_count: int = 0
        self._current_animation: PlayerAnimation = PlayerAnimation.IDLE
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2()
        self.direction: int = 0  # from 0 to 3 clockwise starting to the right

    def update_velocity(self):
        self.rect.topleft += self.velocity
        self.velocity = pygame.math.Vector2()

    @property
    def current_animation(self) -> PlayerAnimation:
        return self._current_animation

    @current_animation.setter
    def current_animation(self, value: PlayerAnimation) -> None:
        if self._current_animation == PlayerAnimation.IDLE and self.animation_count in (1, 2):
            self.rect.move_ip(0, 20)

        self.animation_count = 0
        self._current_animation = value
