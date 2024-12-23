import pygame
from laby.sprite.entity import Entity
from typing import Iterable, Callable, Type
from laby.util.tools import get_image, AssetsLoader, Direction
from laby.util.misc import float_pos
from laby.game_constants import LabGameConstants
from .state import IdleState, PlayerState


class Player(Entity):
    def __init__(self, screen_center: Iterable[float | int], *groups: tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self._move_operation = pygame.Vector2()
        self.velocity = pygame.Vector2()

        image = get_image(pygame.image.load(AssetsLoader().get("player.idle")), (0, 0), LabGameConstants().PLAYER_SIZE,
                          LabGameConstants().PLAYER_SCALE)
        self._state: PlayerState = IdleState(self.set_state_type, self.move, image.get_rect(center=screen_center), image)
        self._state.on_start()

    def get_mask(self) -> pygame.Mask:
        return self._state.mask

    def update_velocity(self) -> None:
        try:
            self.rect.topleft += self.velocity.normalize() * LabGameConstants().SPEED + self._move_operation
        except ValueError:
            self.rect.topleft += self._move_operation
        self.velocity, self._move_operation = pygame.Vector2(), pygame.Vector2()

    def update(self, *args, **kwargs):
        self.update_velocity()
        self._state.update()

    def move(self, xy: float_pos):
        self._move_operation += xy

    def animate(self, event: pygame.event.Event) -> None:
        self._state.animate(event.type)

    # GETTERS AND SETTERS
    # -------------------------------------------------------------
    def state_is(self, state_type: type) -> bool:
        return isinstance(self._state, state_type)

    def get_state_type(self) -> Type[PlayerState]:
        return type(self._state)

    def set_state_type(self, _class: Callable[..., PlayerState]) -> None:
        self._state.on_end()
        self._state = _class(self.set_state_type, *self._state.get_init_args())
        self._state.on_start()

    def get_direction(self) -> Direction:
        return self._state.direction

    def set_direction(self, value: Direction) -> None:
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
        self._state.image = value  # wait why tf would I want to do that ?
