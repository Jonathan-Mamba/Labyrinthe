import numpy as np
import pygame
import icecream
from GameCore.labGameConstants import LabGameConstants as gameConsts
from GameCore.labGameConstants import LabEngineConstants as engineConsts
from GameCore.sprite.player import Player, PlayerAnimation
from GameCore.util import tools

type Event = pygame.event.Event


def player_key_down(event: Event, _, engine_consts: engineConsts):
    # from 0 to 3 clockwise starting to the right
    if event.key in (pygame.K_LEFT, pygame.K_q):
        engine_consts.player.direction = 2
    elif event.key in (pygame.K_RIGHT, pygame.K_d):
        engine_consts.player.direction = 0
    elif event.key in (pygame.K_UP, pygame.K_z):
        engine_consts.player.direction = 3
    elif event.key in (pygame.K_DOWN, pygame.K_s):
        engine_consts.player.direction = 1

    if event.key == pygame.K_SPACE:
        if engine_consts.player.current_animation == PlayerAnimation.IDLE:
            engine_consts.player.current_animation = PlayerAnimation.BASE_ATTACK
        else:
            engine_consts.player.current_animation = PlayerAnimation.IDLE


def video_resize(_, game_consts: gameConsts, engine_consts: engineConsts) -> None:
    game_consts.SCREEN_RES = np.array(pygame.display.get_window_size())
    engine_consts.camera_rect = pygame.Rect(
        [game_consts.CAMERABOX_OFFSET, game_consts.CAMERABOX_OFFSET],
        game_consts.SCREEN_RES - (game_consts.CAMERABOX_OFFSET * 2))


def player_idle(_, __, engine_consts: engineConsts) -> None:
    player: Player = engine_consts.player
    if player.current_animation == PlayerAnimation.IDLE:
        player.animation_count = (player.animation_count + 1) % 5
        player.image = tools.get_image(
            pygame.image.load(f"assets/player/idle.png").convert_alpha(),
            (player.animation_count, player.direction),
            Player.SPRITE_SIZE,
            Player.SCALE_FACTOR
        )
        if player.animation_count == 1:
            player.rect.move_ip(0, -20)
        elif player.animation_count == 3:
            player.rect.move_ip(0, 20)


def debug(event: Event, game_consts: gameConsts, engine_consts: engineConsts):
    if event.key == pygame.K_TAB:
        print(game_consts.lab_array)


def event_quit(_, __, engine_consts: engineConsts) -> None:
    pygame.display.quit()
    pygame.quit()
    engine_consts.is_open = False
