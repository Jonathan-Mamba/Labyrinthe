import fractions

import numpy as np
import pygame
import icecream
from GameCore.labGameConstants import LabGameConstants as gameConsts
from GameCore.sprite.player import Player, PlayerAnimation
from GameCore.util import tools

type Event = pygame.event.Event


def player_key_down(event: Event, game_consts: gameConsts):
    # from 0 to 3 clockwise starting to the right
    if event.key in (pygame.K_LEFT, pygame.K_q):
        game_consts.player.direction = 2
    elif event.key in (pygame.K_RIGHT, pygame.K_d):
        game_consts.player.direction = 0
    elif event.key in (pygame.K_UP, pygame.K_z):
        game_consts.player.direction = 3
    elif event.key in (pygame.K_DOWN, pygame.K_s):
        game_consts.player.direction = 1


def video_resize(_, game_consts: gameConsts) -> None:
    game_consts.SCREEN_RES = np.array(pygame.display.get_window_size())
    game_consts.camera_rect = pygame.Rect(
        [game_consts.CAMERABOX_OFFSET, game_consts.CAMERABOX_OFFSET],
        game_consts.SCREEN_RES - (game_consts.CAMERABOX_OFFSET * 2))


def player_idle(_, game_consts: gameConsts) -> None:
    player: Player = game_consts.player
    if player.current_animation == PlayerAnimation.IDLE:
        player.animation_count = (player.animation_count + 1) % 5
        player.image = tools.get_image(
            pygame.image.load(f"assets/player_{game_consts.player.direction}.png").convert_alpha(),
            (player.animation_count, player.direction),
            Player.SPRITE_SIZE,
            Player.SCALE_FACTOR
        )
        if player.animation_count == 1:
            player.rect.move_ip(0, -20)
        elif player.animation_count == 3:
            player.rect.move_ip(0, 20)


def debug(event: Event, game_consts: gameConsts):
    if event.key == pygame.K_SPACE:
        icecream.ic(game_consts.player.rect.center - game_consts.offset)


def event_quit(_, game_consts: gameConsts) -> None:
    pygame.display.quit()
    pygame.quit()
    game_consts.is_open = False


def mousewheel(event: Event, game_consts: gameConsts) -> None:
    raise PendingDeprecationWarning(">> je garde juste ce truc au cas ou mais je pense je vais l'enlever")
    game_consts.zoom_scale += event.y * game_consts.ZOOM_SCALE_STEP

    if game_consts.zoom_scale <= 0:
        game_consts.zoom_scale = game_consts.ZOOM_SCALE_STEP
    elif game_consts.zoom_scale > fractions.Fraction(2, 1):
        game_consts.zoom_scale = fractions.Fraction(2, 1)
    else:
        print(f"zoom scale: {float(game_consts.zoom_scale)}")
        for group in game_consts.groups:
            for sprite in group:
                sprite.zoom_behavior(game_consts, event.y)
