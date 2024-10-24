import sys
import fractions
import icecream
import numpy as np

sys.path.append("/labyrinthe/GameCore")
import pygame
from GameCore.labGameConstants import LabGameConstants as gameConsts

type Event = pygame.event.Event

def event_quit(_, game_consts: gameConsts) -> None:
    pygame.display.quit()
    pygame.quit()
    game_consts.is_open = False


def key_down(event: Event, game_consts: gameConsts) -> None:
    game_consts.pressed_keys[event.key] = True


def key_up(event: Event, game_consts: gameConsts) -> None:
    game_consts.pressed_keys[event.key] = False


def mousewheel(event: Event, game_consts: gameConsts) -> None:
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
