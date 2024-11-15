import pygame
import typing
from GameCore.sprite.LabSprite import LabSprite
from GameCore.util.misc import int_pos, Direction


class Wall(LabSprite):
    def __init__(self, topleft: int_pos, sides: int, direction: Direction, image_size: int_pos):
        super().__init__()
        rotation_angle: float = 0
        file_path: str = ""
        if direction == Direction.NORTH: rotation_angle = 90
        elif direction == Direction.SOUTH: rotation_angle = 270
        elif direction == Direction.WEST: rotation_angle = 180
        if sides == 1:
            file_path = "assets/wall/wall_3.png"
        elif sides == 3:
            file_path = "assets/wall/wall_3cells.png"

        if file_path:
            self.image = pygame.transform.scale(
                pygame.transform.rotate(pygame.image.load(file_path), rotation_angle), image_size)
        else:
            self.image = pygame.Surface(image_size)
        self.rect = self.image.get_rect(topleft=topleft)
