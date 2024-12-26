import pgtext
import pygame
from laby.constants import LabGameConstants, LabEngineConstants
from laby.util import AssetsLoader
from .collision_engine import CollisionEngine


class Renderer:
    """
    Singleton object which has the sole responsibility of rendering the sprites
    """
    def render(self, game_consts: LabGameConstants, engine_consts: LabEngineConstants):
        pygame.draw.rect(engine_consts.surface, [0, 0, 0], pygame.Rect([0, 0], game_consts.SCREEN_RES))
        for group in engine_consts.groups:
            for sprite in group:
                engine_consts.surface.blit(sprite.image, sprite.rect.topleft - engine_consts.offset)

        pgtext.draw(
            f"{CollisionEngine().collides_wall_or_junction(engine_consts.player.rect, engine_consts.player.get_mask())}",
            (0, 0),
            antialias=False, fontname=AssetsLoader().get("font.minecraft", "ttf"), fontsize=14, background=(0, 0, 0)
        )
