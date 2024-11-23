import enum
import pygame


class CustomEvent(enum.IntEnum):
    PLAYER_IDLE = pygame.event.custom_type()


custom_event_dict: dict = {
    CustomEvent.PLAYER_IDLE: []
}
