import pygame
from laby.sprite.LabSprite import LabSprite
from laby.util.misc import int_pos, Direction
import laby.util.tools as tools
from laby.util import AssetsLoader
import icecream
import colorama
colorama.init(True)


def GRAY() -> str: return colorama.Fore.LIGHTBLACK_EX
def BLUE() -> str: return colorama.Fore.BLUE
def GREEN() -> str: return colorama.Fore.GREEN


class Wall(LabSprite):
    """
    Class that represent a wall of the labyrinth
    """

    def __init__(self, topleft: int_pos, image: pygame.Surface, wall_type: float, _dir: Direction | int = Direction.NONE, *groups):
        """
        this is supposed to be a private constructor so use the static methods pls
        """
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = wall_type  # 0 -> 0, 1 -> 1, 2.0 -> 2.straight, 2.5 -> 2.curved, 3 -> 3, 4 -> 4, 5 -> null
        self.direction = Direction(_dir)

    def __repr__(self) -> str:
        return f"Wall<(type {self.type} to {self.direction.name} at {self.rect.topleft} in {len(self.groups())} groups)>"

    @staticmethod
    def from_one(topleft: int_pos, image_size: int_pos, direction: Direction, *groups) -> 'Wall':
        rotation_angle: float = tools.get_inverse(direction) * -45 + 270  # ax+b
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.transform.rotate(
                            pygame.image.load(AssetsLoader().get("wall.1")).convert_alpha(), rotation_angle
                        ), image_size
                    ),
                    1., direction, *groups
                    )

    @staticmethod
    def from_two(topleft: int_pos, image_size: int_pos, direction: Direction, origin: Direction, *groups) -> 'Wall':
        rotation_angle: float = tools.get_inverse(direction) * -45 + 270  # ax+b
        if tools.get_inverse(direction) == origin:
            path: str = AssetsLoader().get("wall.2.straight")
        else:
            path: str = AssetsLoader().get("wall.2.curved")
            direction_wall_idk = (origin + 1) * (direction + 1)  # tkt ya un schéma dans assets nrmlt # nn la flemme
            if direction_wall_idk == 15: rotation_angle = 0
            elif direction_wall_idk == 3: rotation_angle = 90
            elif direction_wall_idk == 7: rotation_angle = 180
            elif direction_wall_idk == 35: rotation_angle = 270
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.transform.rotate(
                            pygame.image.load(path).convert_alpha(), rotation_angle
                        ), image_size
                    ), 2. if tools.get_inverse(origin) == direction else 2.5, direction, *groups
                    )

    @staticmethod
    def from_three(topleft: int_pos, image_size: int_pos, direction: Direction, *groups) -> 'Wall':
        rotation_angle: float = tools.get_inverse(direction) * -45 + 270  # ax+b
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.transform.rotate(
                            pygame.image.load(AssetsLoader().get("wall.3")).convert_alpha(), rotation_angle
                        ), image_size
                    ), 3., direction, *groups
                    )

    @staticmethod
    def from_four(topleft: int_pos, image_size: int_pos, *groups) -> 'Wall':
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.image.load(AssetsLoader().get("wall.4")).convert_alpha(), image_size
                    ), 4., Direction.NONE, *groups
                    )

    @staticmethod
    def from_zero(topleft: int_pos, image_size: int_pos, *groups) -> 'Wall':
        return Wall(topleft,
                    pygame.transform.scale(
                        pygame.image.load(AssetsLoader().get("wall.0")).convert_alpha(), image_size
                    ), 0., Direction.NONE, *groups
                    )
