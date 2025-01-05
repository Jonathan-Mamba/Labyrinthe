import time
import pgtext
import pygame
from laby.constants import LabGameConstants, LabEngineConstants, GameState
from laby.util import AssetsLoader
from .collision_engine import CollisionEngine


class Renderer:
    """
    Singleton object which has the sole responsibility of rendering the sprites
    """
    def render(self, game_consts: LabGameConstants, engine_consts: LabEngineConstants):
        surface_rect = pygame.Rect([0, 0], game_consts.SCREEN_RES)
        pygame.draw.rect(engine_consts.surface, [0, 0, 0], surface_rect)
        for group in engine_consts.groups:
            for sprite in group:
                if surface_rect.colliderect(sprite.rect.move(*-engine_consts.offset)):
                    engine_consts.surface.blit(sprite.image, sprite.rect.topleft - engine_consts.offset)

        if engine_consts.state == GameState.GAME_LOST:
            pgtext.draw(f"PERDUUUUU", None, sysfontname="calibri", fontsize=60, center=[i/2 for i in game_consts.SCREEN_RES], background=(255, 0, 0))
        elif engine_consts.state == GameState.GAME_WON:
            pgtext.draw(f"GAGNEEEEEEEEEE", None, sysfontname="calibri", fontsize=60, center=[i/2 for i in game_consts.SCREEN_RES], background=(0, 255, 0))
        pgtext.draw(
            f"{engine_consts.player.rect.topleft}\n{engine_consts.max_traversal_duration - round(time.time()) + engine_consts.start_time}",
            (0, 0),
            antialias=True, sysfontname="calibri", fontsize=18, background=(0, 0, 0)
        )
