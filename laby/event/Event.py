import pygame
from typing import Callable
from laby.constants import LabGameConstants as gameConsts
from laby.constants import LabEngineConstants as engineConsts


class EventObserver:
    def __init__(self, func: Callable):
        self.func = func

    def notify(self, event: pygame.event.Event, game_consts: gameConsts):
        self.func(event, game_consts)


class EventSubject:
    default: dict[int, list[EventObserver]] = {
        pygame.QUIT: [],
        pygame.ACTIVEEVENT: [],
        pygame.KEYUP: [],
        pygame.KEYDOWN: [],
        pygame.MOUSEMOTION: [],
        pygame.MOUSEBUTTONUP: [],
        pygame.VIDEORESIZE: [],
        pygame.VIDEOEXPOSE: [],
        pygame.USEREVENT: [],
        pygame.MOUSEWHEEL: [],
    }

    def __init__(self, event_dict: dict[pygame.event.Event, list[EventObserver]] = None) -> None:
        if event_dict is None:
            self.event_dict = EventSubject.default
        else:
            self.event_dict = event_dict | EventSubject.default  # fuses the dicts with the first one in priority

    def notify(self, event: pygame.event.Event, game_consts: gameConsts) -> None:
        observers = self.event_dict.get(event.type, None)
        if observers:
            for observer in observers:
                observer.notify(event, game_consts)

    def add_observer(self, observer: EventObserver, event_type: int) -> bool:
        """returns True if observer is not found, else returns False"""
        observers = self.event_dict.get(event_type)
        if observer in observers:
            return False
        observers.append(observer)
        return True

    def remove_observer(self, observer: EventObserver) -> None:
        for observers in self.event_dict.values():
            if observer in observers:
                observers.remove(observer)
