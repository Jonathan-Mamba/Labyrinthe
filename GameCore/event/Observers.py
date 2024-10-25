import fractions
import pygame
from GameCore.labGameConstants import LabGameConstants as gameConsts
from GameCore.sprite.player import Player, PlayerAnimation

type Event = pygame.event.Event


def player_idle(_, game_consts: gameConsts) -> None:
    player: Player = game_consts.player_group.sprite
    if player.current_animation == PlayerAnimation.IDLE:
        player.animation_count = (player.animation_count + 1) % 5
        player.image = player.get_image(
            pygame.image.load("assets/player.png"),
            (player.animation_count, 0),
            Player.SPRITE_SIZE,
            scale_factor=Player.SCALE_FACTOR
        )
        if player.animation_count == 1:
            player.rect.move_ip(0, -20)
        elif player.animation_count == 3:
            player.rect.move_ip(0, 20)


def get_fps(event: Event, game_consts: gameConsts):
    if event.key == pygame.K_SPACE:
        print(game_consts.clock.get_fps())


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
