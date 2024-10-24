import sys

sys.path.append("C:/Users/jojod/Bureau/fichiers_python/autres")
from labyrinthe.GameCore.Event import Event, Observers
from labyrinthe.GameCore import labGameConstants as gameConsts
from labyrinthe.GameCore.Sprite.cell import Cell
import pygame


class LabGameEngine:
    def __init__(self, game_constants: gameConsts.LabGameConstants, event_subject: Event.EventSubject):
        self.game_constants: gameConsts.LabGameConstants = game_constants
        self.event_subject: Event.EventSubject = event_subject

    def at_startup(self) -> None:
        self.game_constants.surface = pygame.display.set_mode(self.game_constants.screen_res)
        pygame.display.set_caption(self.game_constants.title)
        self.game_constants.LAB_RECT = pygame.Rect(self.game_constants.offset,
                                                   self.game_constants.LAB_SIZE * self.game_constants.CELL_WIDTH + (
                                                   (self.game_constants.LAB_SIZE - 1) * self.game_constants.BORDER_WIDTH))
        self.create_cells()
        self.add_observers()

    def create_cells(self) -> None:
        for index, value in enumerate(self.game_constants.labyrinth):
            cell = Cell(game_consts=self.game_constants, index=index,
                        pos=(value * self.game_constants.CELL_WIDTH + (value * self.game_constants.BORDER_WIDTH)))
            cell.align_to_previous()
            self.game_constants.cells_group.add(cell)

    def add_observers(self):
        self.event_subject.add_observer(Event.EventObserver(Observers.event_quit), pygame.QUIT)
        self.event_subject.add_observer(Event.EventObserver(Observers.key_down), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.key_up), pygame.KEYUP)
        self.event_subject.add_observer(Event.EventObserver(Observers.mousewheel), pygame.MOUSEWHEEL)

    def update(self) -> None:
        if self.game_constants.pressed_keys.get(pygame.K_LEFT) or self.game_constants.pressed_keys.get(pygame.K_q):
            self.game_constants.offset[0] += self.game_constants.OFFSET_STEP
        elif self.game_constants.pressed_keys.get(pygame.K_RIGHT) or self.game_constants.pressed_keys.get(pygame.K_d):
            self.game_constants.offset[0] -= self.game_constants.OFFSET_STEP
        elif self.game_constants.pressed_keys.get(pygame.K_UP) or self.game_constants.pressed_keys.get(pygame.K_z):
            self.game_constants.offset[1] += self.game_constants.OFFSET_STEP
        elif self.game_constants.pressed_keys.get(pygame.K_DOWN) or self.game_constants.pressed_keys.get(pygame.K_s):
            self.game_constants.offset[1] -= self.game_constants.OFFSET_STEP

        pygame.draw.rect(self.game_constants.surface, [0, 0, 0], pygame.Rect([0, 0], self.game_constants.screen_res))
        for group in self.game_constants.groups:
            group.update(self.game_constants)
            group.draw(self.game_constants.surface)




    def main(self):
        pygame.init()
        self.at_startup()
        self.game_constants.is_open = True
        while self.game_constants.is_open:
            self.update()
            pygame.display.flip()
            for event in pygame.event.get():
                self.event_subject.notify(event, self.game_constants)


if __name__ == "__main__":
    LabGameEngine(gameConsts.LabGameConstants(), Event.EventSubject()).main()
