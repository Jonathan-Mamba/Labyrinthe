import pygame
from laby.sprite.LabSprite import LabSprite
from laby.util.misc import int_pos, Direction
import laby.util.tools as tools
from laby.util import AssetsLoader


class Wall(LabSprite):
    """
    Class that represent a wall of the labyrinth
    """
    def __init__(self, topleft: int_pos, image: pygame.Surface):
        """
        this is supposed to be a private constructor so use the static methods pls
        """
        super().__init__()
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect(topleft=topleft)
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def from_one(topleft: int_pos, image_size: int_pos, direction: Direction) -> 'Wall':
        rotation_angle: float = tools.get_inverse(direction) * -45 + 270  # ax+b
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.transform.rotate(
                            pygame.image.load(AssetsLoader().get("wall.1")).convert_alpha(), rotation_angle
                        ), image_size
                    ))

    @staticmethod
    def from_two(topleft: int_pos, image_size: int_pos, direction: Direction, origin: Direction) -> 'Wall':
        rotation_angle: float = tools.get_inverse(direction) * -45 + 270  # ax+b
        if tools.get_inverse(direction) == origin:
            path: str = AssetsLoader().get("wall.2.straight")
        else:
            path:str = AssetsLoader().get("wall.2.curved")
            direction_wall_idk = (origin + 1) * (direction + 1)  # tkt ya un schéma dans assets/schémas normalement
            if direction_wall_idk == 15: rotation_angle = 0
            elif direction_wall_idk == 3: rotation_angle = 90
            elif direction_wall_idk == 7: rotation_angle = 180
            elif direction_wall_idk == 35: rotation_angle = 270
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.transform.rotate(
                            pygame.image.load(path).convert_alpha(), rotation_angle
                        ), image_size
                    ))

    @staticmethod
    def from_three(topleft: int_pos, image_size: int_pos, direction: Direction) -> 'Wall':
        rotation_angle: float = tools.get_inverse(direction) * -45 + 270  # ax+b
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.transform.rotate(
                            pygame.image.load(AssetsLoader().get("wall.3")).convert_alpha(), rotation_angle
                        ), image_size
                    ))

    @staticmethod
    def from_four(topleft: int_pos, image_size: int_pos) -> 'Wall':
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.image.load(AssetsLoader().get("wall.4")).convert_alpha(), image_size
                    ))

    @staticmethod
    def from_zero(topleft: int_pos, image_size: int_pos) -> 'Wall':
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.image.load(AssetsLoader().get("wall.0")).convert_alpha(), image_size
                    ))


