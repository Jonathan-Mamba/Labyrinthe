import pygame
from laby.constants import LabGameConstants, LabEngineConstants


class Renderer:
    """
    Singleton object which has the sole responsibility of rendering the sprites
    """
    def render(self, game_consts: LabGameConstants, engine_consts: LabEngineConstants):
        pygame.draw.rect(engine_consts.surface, [0, 0, 0], pygame.Rect([0, 0], game_consts.SCREEN_RES))
        for group in engine_consts.groups:
            group.update(game_consts)
            for sprite in group:
                engine_consts.surface.blit(sprite.image, -engine_consts.offset + sprite.rect.topleft)
