import pygame
from GameCore.sprite.LabSprite import LabSprite


class Junction(LabSprite):
    def __init__(self, cell_width: int, border_width: int, color: pygame.Color, vertical: bool, topleft, *groups):
        super().__init__(*groups)
        self.is_vertical = vertical
        _str: str = "horizontal" if vertical else "vertical"  # jsp j'ai pas compris
        size = (border_width, cell_width) if vertical else (cell_width, border_width)

        self.image: pygame.Surface = (pygame.Surface(size))
        self.image.fill(color)
        self.image.blit(
            pygame.transform.scale(pygame.image.load(f"assets/junction/{_str}.png").convert_alpha(), size),
            (0, 0)
        )
        self.rect = self.image.get_rect(topleft=topleft)

    def __repr__(self) -> str:
        return f"<Junction({self.rect.topleft}, {self.is_vertical})>"
