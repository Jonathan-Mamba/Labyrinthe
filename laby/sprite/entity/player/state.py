import pygame
from typing import Callable, final
from laby.event.custom import CustomEvent
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
            mask = pygame.Mask(LabGameConstants().PLAYER_SIZE * LabGameConstants().PLAYER_SCALE, True)

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
            LabGameConstants().PLAYER_SIZE,
            LabGameConstants().PLAYER_SCALE
        )
        if self.animation_count == 1:
            self.mover((0., (LabGameConstants().PLAYER_SCALE - .5) * -10))
        elif self.animation_count == 3:
            self.mover((0., (LabGameConstants().PLAYER_SCALE - .5) * 10))
        self.animation_count = (self.animation_count + 1) % 5


class BaseAttackState(PlayerState):
    def animate(self, event: int): pass


