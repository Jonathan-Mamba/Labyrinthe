import pygame
import numpy as np
from laby.constants import LabGameConstants, LabEngineConstants
from laby.sprite.entity.player import IdleState, BaseAttackState
from laby.util import AssetsAccessor
from pprint import pprint

type Event = pygame.event.Event


class EngineObserver:
    """
    Singleton object which contains observers that need access to LabEngineConstants()
    """
    def __init__(self, engine_consts: LabEngineConstants):
        self.engine_consts = engine_consts


    def event_quit(self, _, __) -> None:
        pygame.display.quit()
        pygame.quit()
        self.engine_consts.is_open = False


    def video_resize(self, _, game_consts: LabGameConstants) -> None:
        game_consts.SCREEN_RES = np.array(pygame.display.get_window_size())
        self.engine_consts.camera_rect = pygame.Rect(
            [game_consts.CAMERABOX_OFFSET, game_consts.CAMERABOX_OFFSET],
            game_consts.SCREEN_RES - (game_consts.CAMERABOX_OFFSET * 2))


    def player_key_down(self, event: Event, _) -> None:
        if event.key == pygame.K_SPACE:
            if self.engine_consts.player.state_is(IdleState):
                self.engine_consts.player.set_state_type(BaseAttackState)
            else:
                self.engine_consts.player.set_state_type(IdleState)


    def debug(self, event: Event, game_consts: LabGameConstants) -> None:
        if event.key == pygame.K_TAB:
            print(AssetsAccessor())
