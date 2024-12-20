import pygame
from laby.sprite.LabSprite import LabSprite
from laby.util.misc import int_pos, Direction
import laby.util.tools as tools


class Wall(LabSprite):
    def __init__(self, topleft: int_pos, sides: int, direction: Direction, image_size: int_pos, origin: Direction | None = None):
        super().__init__()
        rotation_angle: float = 0
        file_path: str = ""
        if direction == Direction.NORTH: rotation_angle = 90
        elif direction == Direction.SOUTH: rotation_angle = 270
        elif direction == Direction.WEST: rotation_angle = 180

        if sides == 1 or sides == 3:
            file_path = f"assets/wall/{sides}edges_wall.png"
        elif sides == 2 and origin is None:
            raise ValueError("c'est pas possible de créer un wall aec deux cotes sans origine")
        elif sides == 2 and origin is not None:
            # si c'est un mur en ligne
            if tools.get_inverse_direction(direction) == origin:
                file_path = "assets/wall/2edges_wall_linear.png"
            else:
                file_path = "assets/wall/2edges_wall_angle.png"
                dir = (origin + 1) * (direction + 1) # tkt ya un schéma dans assets/schémas normalement
                if dir == 15: rotation_angle = 0
                elif dir == 3: rotation_angle = 90
                elif dir == 7: rotation_angle = 180
                elif dir == 35: rotation_angle = 270

        if file_path:
            self.image = pygame.transform.scale(
                pygame.transform.rotate(pygame.image.load(file_path).convert_alpha(), rotation_angle), image_size)
        else:
            self.image = pygame.Surface(image_size)
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=topleft)
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)
