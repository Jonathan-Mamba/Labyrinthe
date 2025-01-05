import pygame
from laby.sprite.LabSprite import LabSprite
from laby.util import AssetsLoader
from laby.game_constants import LabGameConstants


class Junction(LabSprite):
    _VERTICAL_MASK: pygame.Mask = None
    _HORIZONTAL_MASK: pygame.Mask = None

    def __init__(self, cell_width: int, border_width: int, color: pygame.Color, vertical: bool, topleft, *groups):
        super().__init__(*groups)
        self.is_vertical = vertical
        _str: str = "vertical" if vertical else "horizontal"
        size = (cell_width, border_width) if vertical else (border_width, cell_width)

        self.image: pygame.Surface = (pygame.Surface(size))
        self.image.fill(color)
        self.image.blit(
            pygame.transform.scale(pygame.image.load(AssetsLoader().get(f"junction.{_str}")).convert_alpha(), size),
            (0, 0)
        )
        self.rect = self.image.get_rect(topleft=topleft)

    def __repr__(self) -> str:
        return f"<Junction({self.rect.topleft}, {self.is_vertical})>"

    @property
    def mask(self) -> pygame.Mask:
        return self.__class__.get_vertical_mask() if self.is_vertical else self.__class__.get_horizontal_mask()

    @classmethod
    def get_vertical_mask(cls) -> pygame.Mask:
        if cls._VERTICAL_MASK is None:
            cls._VERTICAL_MASK = pygame.mask.from_surface(
                pygame.transform.scale(
                    pygame.image.load(AssetsLoader().get("junction.vertical")).convert_alpha(),
                    (LabGameConstants().CELL_WIDTH, LabGameConstants().BORDER_WIDTH)
                )
            )
        return cls._VERTICAL_MASK

    @classmethod
    def get_horizontal_mask(cls) -> pygame.Mask:
        if cls._HORIZONTAL_MASK is None:
            cls._HORIZONTAL_MASK = pygame.mask.from_surface(pygame.transform.scale(
                pygame.image.load(AssetsLoader().get("junction.horizontal")).convert_alpha(),
                (LabGameConstants().BORDER_WIDTH, LabGameConstants().CELL_WIDTH)
            ))
        return cls._HORIZONTAL_MASK
