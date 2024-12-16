import numpy as np
import pygame
import threading
import icecream
import math
from GameCore.constants import LabGameConstants as gameConsts
from GameCore.constants import LabEngineConstants as engineConsts
from GameCore.sprite.player import Player, PlayerAnimation, IdleState, BaseAttackState
from GameCore.util import tools

type Event = pygame.event.Event


def player_key_down(event: Event, _, engine_consts: engineConsts):
    # from 0 to 3 clockwise starting to the right
    if event.key in (pygame.K_LEFT, pygame.K_q):
        engine_consts.player.set_direction(tools.Direction.WEST)
    elif event.key in (pygame.K_RIGHT, pygame.K_d):
        engine_consts.player.set_direction(tools.Direction.EAST)
    elif event.key in (pygame.K_UP, pygame.K_z):
        engine_consts.player.set_direction(tools.Direction.NORTH)
    elif event.key in (pygame.K_DOWN, pygame.K_s):
        engine_consts.player.set_direction(tools.Direction.SOUTH)

    if event.key == pygame.K_SPACE:
        if engine_consts.player.get_state() is IdleState:
            engine_consts.player.set_state(BaseAttackState)
        else:
            engine_consts.player.set_state(IdleState)


def video_resize(_, game_consts: gameConsts, engine_consts: engineConsts) -> None:
    game_consts.SCREEN_RES = np.array(pygame.display.get_window_size())
    engine_consts.camera_rect = pygame.Rect(
        [game_consts.CAMERABOX_OFFSET, game_consts.CAMERABOX_OFFSET],
        game_consts.SCREEN_RES - (game_consts.CAMERABOX_OFFSET * 2))


def debug(event: Event, game_consts: gameConsts, engine_consts: engineConsts):
    if event.key == pygame.K_TAB:
        print(game_consts.branch_array, "\n-----------------------------")
        print(game_consts.lab_array)
    if event.key == pygame.K_p:
        threading.Thread(target=lambda: print(engine_consts.cells_group.sprites()[int(input("index: "))].edges)).start()


def event_quit(_, __, engine_consts: engineConsts) -> None:
    pygame.display.quit()
    pygame.quit()
    engine_consts.is_open = False
