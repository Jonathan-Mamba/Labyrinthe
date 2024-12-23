import pgtext
import pygame
from typing import Sequence
from laby.constants import LabGameConstants, LabEngineConstants


class Renderer:
    """
    Singleton object which has the sole responsibility of rendering the sprites
    """
    def render(self, game_consts: LabGameConstants, engine_consts: LabEngineConstants):
        pygame.draw.rect(engine_consts.surface, [0, 0, 0], pygame.Rect([0, 0], game_consts.SCREEN_RES))
        for group in engine_consts.groups:
            for sprite in group:
                engine_consts.surface.blit(sprite.image, sprite.rect.topleft - engine_consts.offset)

        wall_collision = engine_consts.player.rect.collidelist([i.rect for i in engine_consts.wall_group.sprites()])
        junction_collision = engine_consts.player.rect.collidelist([i.rect for i in engine_consts.junction_group.sprites()])
        pgtext.draw(f"collided wall: {wall_collision}", (0, 0), owidth=1, ocolor=(0, 0, 0), sysfontname="Segoe UI", fontsize=16)
        pgtext.draw(f"collided junction: {junction_collision}", (0, 15), owidth=1, ocolor=(0, 0, 0), sysfontname="Segoe UI", fontsize=16)
