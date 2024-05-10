import GameCore.GameEngine
from GameCore import gameConstants
from GameCore import Event


class LabGameEngine(GameCore.GameEngine.GameEngine):

    def __init__(self, game_constants: gameConstants.GameConstants, engine_constants: gameConstants.EngineConstants,
                 event_subject: Event.EventSubject):
        super().__init__(game_constants, engine_constants, event_subject)

    def at_startup(self): ...

    def update(self): ...


if __name__ == "__main__":
    LabGameEngine()
