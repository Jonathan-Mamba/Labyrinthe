import pygame
from typing import Callable


class EventObserver:
    def __init__(self, func: Callable):
        self.func = func

    def notify(self, event):
        self.func(event)


class EventSubject:
    default: dict[pygame.event.Event, list[EventObserver]] = dict.fromkeys([
        pygame.QUIT,
        pygame.ACTIVEEVENT,
        pygame.KEYUP,
        pygame.KEYDOWN,
        pygame.MOUSEMOTION,
        pygame.MOUSEBUTTONUP,
        pygame.JOYAXISMOTION,
        pygame.JOYBALLMOTION,
        pygame.JOYHATMOTION,
        pygame.JOYBUTTONUP,
        pygame.JOYBUTTONDOWN,
        pygame.VIDEORESIZE,
        pygame.VIDEOEXPOSE,
        pygame.USEREVENT
    ], [])

    def __init__(self, event_dict: dict[pygame.event.Event, list[EventObserver]] = None) -> None:
        if event_dict is None:
            event_dict = EventSubject.default
        self.event_dict = event_dict | EventSubject.default

    def notify(self, event) -> None:
        observers = self.event_dict.get(event, None)
        if observers:
            for observer in observers:
                observer.notify(event)

    def add_observer(self, observer: EventObserver, event: pygame.event.Event) -> bool:
        observers = self.event_dict[event]
        if observer in observers:
            return False
        observers.append(observer)
        return True

    def remove_observer(self, observer: EventObserver):
        for event, observers in self.event_dict.items():
            if observer in observers:
                observers.remove(observer)

