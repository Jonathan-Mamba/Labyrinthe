import numpy as np
import pygame
from laby.constants import LabGameConstants, LabEngineConstants
from laby.util import MetaSingleton
from laby.sprite import Wall, Junction


class CollisionEngine(metaclass=MetaSingleton):
    """
    idk all of the things related to collision
    this class should be called from anywhere for example to check if the player will collide with anything
    """
    def __init__(self, ec: LabEngineConstants = None):
        self._engine_constants = ec

    def collides_wall_or_junction(self, rect: pygame.Rect, mask: pygame.Mask) -> bool:
        collides_wall = False
        collides_junction = False

        collided_wall: int = rect.collidelist([i.rect for i in self._engine_constants.wall_group.sprites()])
        collided_junction: int = rect.collidelist([i.rect for i in self._engine_constants.junction_group.sprites()])

        if collided_wall > -1:
            wall: Wall = self._engine_constants.wall_group.sprites()[collided_wall]
            if wall.mask.overlap(mask, np.array(rect.topleft) - wall.rect.topleft) is not None:
                collides_wall = True  # I could put this in one line but YOU would get a headache atp

        if collided_junction > -1:
            junction: Junction = self._engine_constants.junction_group.sprites()[collided_junction]
            if junction.mask.overlap(mask, np.array(rect.topleft) - junction.rect.topleft) is not None:
                collides_junction = True

        return collides_junction or collides_wall

    def update(self):
        pass
