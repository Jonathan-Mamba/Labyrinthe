import abc
import pygame
from labyrinthe.gameImplemtation import Event

import gameConstants


class GameEngine(abc.ABC):
    def __init__(self, game_constants: gameConstants.GameConstants, engine_constants: gameConstants.EngineConstants,
                 event_subject: Event.EventSubject) -> None:
        self.game_constants = game_constants
        self.engine_constants = engine_constants
        self.event_subject = event_subject

    def __at_startup(self) -> None:
        pass

    @abc.abstractmethod
    def at_startup(self):
        ...

    @abc.abstractmethod
    def update(self):
        ...

    def main(self):
        pygame.init()
        self.__at_startup()
        self.at_startup()
        is_open = True
        while is_open:
            self.update()
            pygame.display.flip()
            for event in pygame.event.get():
                self.event_subject.notify(event)
