import pygame
import numpy as np
from laby.constants import LabEngineConstants, LabGameConstants
from laby.sprite.entity.player import IdleState, BaseAttackState
from pprint import pprint
import icecream

type Event = pygame.event.Event


class EngineObserver:
    """
    Singleton object which contains observers that need access to LabEngineConstants()
    """
    def __init__(self, engine_consts: LabEngineConstants):
        self.engine_consts = engine_consts


    def event_quit(self, _) -> None:
        pygame.display.quit()
        pygame.quit()
        self.engine_consts.is_open = False


    def video_resize(self, _) -> None:
        game_consts = LabGameConstants()
        game_consts.SCREEN_RES = np.array(pygame.display.get_window_size())
        self.engine_consts.camera_rect = pygame.Rect(
            [game_consts.CAMERABOX_OFFSET, game_consts.CAMERABOX_OFFSET],
            game_consts.SCREEN_RES - (game_consts.CAMERABOX_OFFSET * 2))


    def player_key_down(self, event: Event,) -> None:
        if event.key == pygame.K_SPACE:
            if self.engine_consts.player.state_is(IdleState):
                self.engine_consts.player.set_state_type(BaseAttackState)
            else:
                self.engine_consts.player.set_state_type(IdleState)


    def debug(self, event: Event) -> None:
        if event.key == pygame.K_TAB:
            print(LabGameConstants().lab_array)
        elif event.key == pygame.K_RETURN:
            print(self.engine_consts.player.rect.collidelist(
                [cell.rect for cell in self.engine_consts.cells_group.sprites()]))
