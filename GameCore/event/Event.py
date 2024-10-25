import pprint

import pygame
from typing import Callable
import sys

sys.path.append("/labyrinthe/GameCore")
import GameCore.labGameConstants as gameConsts


class EventObserver:
    def __init__(self, func: Callable):
        self.func = func

    def notify(self, event: pygame.event.Event, game_consts: gameConsts.LabGameConstants):
        self.func(event, game_consts)


class EventSubject:
    default: dict[int, list[EventObserver]] = {
        pygame.QUIT: [],
        pygame.ACTIVEEVENT: [],
        pygame.KEYUP: [],
        pygame.KEYDOWN: [],
        pygame.MOUSEMOTION: [],
        pygame.MOUSEBUTTONUP: [],
        pygame.JOYAXISMOTION: [],
        pygame.JOYBALLMOTION: [],
        pygame.JOYHATMOTION: [],
        pygame.JOYBUTTONUP: [],
        pygame.JOYBUTTONDOWN: [],
        pygame.VIDEORESIZE: [],
        pygame.VIDEOEXPOSE: [],
        pygame.USEREVENT: [],
        pygame.MOUSEWHEEL: []
    }

    def __init__(self, event_dict: dict[pygame.event.Event, list[EventObserver]] = None) -> None:
        if event_dict is None:
            event_dict = EventSubject.default
        self.event_dict = event_dict | EventSubject.default  # fusionne les deux dictionnaires avec le premier en priorité dans les merge conflits

    def notify(self, event: pygame.event.Event, game_consts: gameConsts.LabGameConstants) -> None:
        observers = self.event_dict.get(event.type, None)
        if observers:
            for observer in observers:
                observer.notify(event, game_consts)

    def add_observer(self, observer: EventObserver, event_type: int) -> bool:
        observers = self.event_dict.get(event_type)
        if observer in observers:
            return False
        observers.append(observer)
        return True

    def remove_observer(self, observer: EventObserver) -> None:
        for observers in self.event_dict.values():
            if observer in observers:
                observers.remove(observer)
