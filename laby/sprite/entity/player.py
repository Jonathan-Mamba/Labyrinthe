import pygame
from typing import Callable, Iterable, Type, final
from laby.event.custom import CustomEvent
from laby.sprite.entity import Entity
from laby.util import tools, AssetsLoader
from laby.util.tools import Direction
from laby.util.misc import float_pos
from laby.game_constants import LabGameConstants


class PlayerState:
    @final
    def __init__(self,
                 state_setter: Callable[[Callable[..., 'PlayerState']], None],
                 mover: Callable[[float_pos], None],
                 rect: pygame.Rect,
                 image: pygame.Surface,
                 count: int = 0,
                 direction: Direction = Direction.EAST,
                 mask: pygame.Mask = None):

        if mask is None:
            mask = pygame.Mask(Player.SPRITE_SIZE * Player.SCALE_FACTOR, True)

        self.state_setter = state_setter
        self.mover = mover
        self.rect = rect
        self.image = image
        self.animation_count = count
        self.direction = direction
        self.mask = mask

    @final
    def get_init_args(self) -> tuple:
        return self.state_setter, self.mover, self.rect, self.image, self.animation_count, self.direction, self.mask

    def animate(self, event: int): ...
    def update(self): ...
    def on_start(self): ...
    def on_end(self): self.animation_count = 0


class IdleState(PlayerState):
    def animate(self, event: int):
        if event != CustomEvent.PLAYER_IDLE:
            return

        self.image = tools.get_image(
            pygame.image.load(AssetsLoader().get("player.idle")).convert_alpha(),
            (self.animation_count, tools.get_anticlockwise(self.direction, 2) / 2),
            Player.SPRITE_SIZE,
            Player.SCALE_FACTOR
        )
        if self.animation_count == 1:
            self.mover((0., (Player.SCALE_FACTOR - .5) * -10))
        elif self.animation_count == 3:
            self.mover((0., (Player.SCALE_FACTOR - .5) * 10))
        self.animation_count = (self.animation_count + 1) % 5


class BaseAttackState(PlayerState):
    def animate(self, event: int): pass


class Player(Entity):
    SPRITE_SIZE = pygame.Vector2(25, 21)
    SCALE_FACTOR = 2

    def __init__(self, screen_center: Iterable[float | int], *groups: tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        image = tools.get_image(pygame.image.load(AssetsLoader().get("player.idle")), (0, 0), Player.SPRITE_SIZE,
                                Player.SCALE_FACTOR)
        self._move_operation = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self._state: PlayerState = IdleState(self.set_state_type, self.move, image.get_rect(center=screen_center), image)
        self._state.on_start()

    def get_mask(self) -> pygame.Mask:
        return self._state.mask

    def update_velocity(self) -> None:
        try: self.rect.topleft += self.velocity.normalize() * LabGameConstants().SPEED + self._move_operation
        except ValueError: self.rect.topleft += self._move_operation
        self.velocity, self._move_operation = pygame.Vector2(), pygame.Vector2()

    def update(self, *args, **kwargs):
        self.update_velocity()
        self._state.update()

    def move(self, xy: float_pos):
        self._move_operation += xy

    def animate(self, event: pygame.event.Event) -> None:
        self._state.animate(event.type)

    # GETTERS AND SETTERS
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

