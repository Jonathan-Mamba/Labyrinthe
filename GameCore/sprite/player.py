import icecream
import numpy as np
import pygame
import typing as t
from GameCore.event.custom import CustomEvent
import enum
from GameCore.sprite.LabSprite import LabSprite
from GameCore.util import tools
from GameCore.util.tools import Direction


class PlayerState:
    def __init__(self, rect: pygame.Rect, image: pygame.Surface, count: int = 0, direction: Direction = Direction.EAST):
        self.rect = rect
        self.image = image
        self.animation_count = count
        self.direction: Direction = direction

    def animate(self, event: int): ...
    def on_start(self): ...
    def on_end(self): self.animation_count = 0


class IdleState(PlayerState):
    def animate(self, event: int):
        if event != CustomEvent.PLAYER_IDLE:
            return

        self.image = tools.get_image(
            pygame.image.load(f"assets/player/idle.png").convert_alpha(),
            (self.animation_count, tools.get_anticlockwise(self.direction, 2) / 2),
            Player.SPRITE_SIZE,
            Player.SCALE_FACTOR
        )
        if self.animation_count == 1:
            self.rect.move_ip(0, -20)
        elif self.animation_count == 3:
            self.rect.move_ip(0, 20)
        self.animation_count = (self.animation_count + 1) % 5


class BaseAttackState(PlayerState):
    def animate(self, event: int): pass


class PlayerAnimation(enum.Enum):
    IDLE = enum.auto()
    BASE_ATTACK = enum.auto()


class Player(LabSprite):
    SPRITE_SIZE = (25, 21)
    SCALE_FACTOR = 3

    def __init__(self, screen_center: t.Iterable[float | int], *groups: tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        image = tools.get_image(pygame.image.load("assets/player/idle.png"), (0, 0), Player.SPRITE_SIZE,
                                Player.SCALE_FACTOR)
        self._state: PlayerState = IdleState(image.get_rect(center=screen_center), image)
        self._state.on_start()
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2()

    def update_velocity(self):
        self.rect.topleft += self.velocity
        self.velocity = pygame.math.Vector2()

    def animate(self, event: pygame.event.Event, *_):
        self._state.animate(event.type)

    def get_state(self) -> t.Type[PlayerState]:
        return type(self._state)

    def set_state(self, value: t.Callable[..., PlayerState]) -> None:
        self._state.on_end()
        self._state = value(self.rect, self.image, self._state.animation_count, self._state.direction)
        self._state.on_start()

    def get_direction(self) -> Direction:
        return self._state.direction

    def set_direction(self, value: Direction):
        self._state.direction = value

    @property
    def rect(self) -> pygame.Rect:
        return self._state.rect

    @rect.setter
    def rect(self, value: pygame.Rect) -> None:
        self._state.rect = value

    @property
    def image(self) -> pygame.Surface:
        return self._state.image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        self._state.image = value
