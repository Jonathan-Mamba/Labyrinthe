import pygame
from GameCore.sprite.LabSprite import LabSprite


class Junction(LabSprite):
    def __init__(self, cell_width: int, border_width: int, color: pygame.Color, vertical: bool, topleft, *groups):
        super().__init__(*groups)
        self.is_vertical = vertical
        if vertical:
            self.image = pygame.Surface((border_width, cell_width))
        else:
            self.image = pygame.Surface((cell_width, border_width))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=topleft)

    def __repr__(self) -> str:
        return f"<Junction({self.rect.topleft}, {self.is_vertical})>"
