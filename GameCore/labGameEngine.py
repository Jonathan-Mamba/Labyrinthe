import numpy as np
import icecream
from GameCore.event import Event, Observers
from GameCore import labGameConstants as gameConsts
from GameCore.sprite.cell import Cell
from GameCore.sprite.player import Player
from GameCore.event.custom import custom_event_dict, CustomEvent
import pygame


class LabGameEngine:
    def __init__(self, game_constants: gameConsts.LabGameConstants, event_subject: Event.EventSubject) -> None:
        self.game_constants: gameConsts.LabGameConstants = game_constants
        self.event_subject: Event.EventSubject = event_subject

    def at_startup(self) -> None:
        self.game_constants.surface = pygame.display.set_mode(self.game_constants.SCREEN_RES, pygame.RESIZABLE)
        pygame.display.set_caption(self.game_constants.title)

        self.game_constants.player_group.sprite = Player(self.game_constants.SCREEN_RES / 2)
        self.game_constants.LAB_RECT = pygame.Rect(self.game_constants.offset,  # pk c'est là ?
                                                   self.game_constants.LAB_SIZE * self.game_constants.CELL_WIDTH + (
                                                   (self.game_constants.LAB_SIZE - 1) * self.game_constants.BORDER_WIDTH))

        pygame.time.set_timer(pygame.event.Event(CustomEvent.PLAYER_IDLE.value), 100)

        self.create_cells()
        self.add_observers()

    def create_cells(self) -> None:
        for index, value in enumerate(self.game_constants.labyrinth):
            cell = Cell(game_consts=self.game_constants, index=index,
                        pos=(value * self.game_constants.CELL_WIDTH + (value * self.game_constants.BORDER_WIDTH)))
            cell.align_to_previous()
            self.game_constants.cells_group.add(cell)

    def add_observers(self) -> None:
        self.event_subject.add_observer(Event.EventObserver(Observers.event_quit), pygame.QUIT)
        self.event_subject.add_observer(Event.EventObserver(Observers.key_down), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.debug), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.key_up), pygame.KEYUP)
        self.event_subject.add_observer(Event.EventObserver(Observers.mousewheel), pygame.MOUSEWHEEL)
        self.event_subject.add_observer(Event.EventObserver(Observers.player_idle), CustomEvent.PLAYER_IDLE.value)

    def process_movement(self) -> None:

        pressed_keys = pygame.key.get_pressed()
        if self.game_constants.pressed_keys.get(pygame.K_LEFT) or self.game_constants.pressed_keys.get(pygame.K_q):
            self.game_constants.player.velocity.x -= self.game_constants.OFFSET_STEP
        if self.game_constants.pressed_keys.get(pygame.K_RIGHT) or self.game_constants.pressed_keys.get(pygame.K_d):
            self.game_constants.player.velocity.x += self.game_constants.OFFSET_STEP
        if self.game_constants.pressed_keys.get(pygame.K_UP) or self.game_constants.pressed_keys.get(pygame.K_z):
            self.game_constants.player.velocity.y -= self.game_constants.OFFSET_STEP
        if self.game_constants.pressed_keys.get(pygame.K_DOWN) or self.game_constants.pressed_keys.get(pygame.K_s):
            self.game_constants.player.velocity.y += self.game_constants.OFFSET_STEP

        try:
            self.game_constants.player.velocity = (
                    self.game_constants.player.velocity.normalize() * self.game_constants.OFFSET_STEP)
        except ValueError:
            pass
        self.game_constants.player.update()


        player_x, player_y = self.game_constants.player.rect.center
        player_rect = self.game_constants.player.rect
        camera_rect = self.game_constants.camera_rect

        if player_x < camera_rect.left:
            camera_rect.left = player_rect.left
            icecream.ic(self.game_constants.player.rect.left == self.game_constants.camera_rect.left)

        if player_x > camera_rect.right:
            camera_rect.right = player_rect.right
            icecream.ic(self.game_constants.player.rect.right == self.game_constants.camera_rect.right)

        if player_y > camera_rect.bottom:
            camera_rect.bottom = player_rect.bottom

        if player_y < camera_rect.top:
            camera_rect.top = player_rect.top

        self.game_constants.offset = np.array((
                                               camera_rect.left - self.game_constants.CAMERABOX_OFFSET,
                                               camera_rect.top - self.game_constants.CAMERABOX_OFFSET,
                                               ))

    def update(self) -> None:
        self.process_movement()
        pygame.draw.rect(self.game_constants.surface, [0, 0, 0], pygame.Rect([0, 0], self.game_constants.SCREEN_RES))
        for group in self.game_constants.groups:
            group.update(self.game_constants)
            for sprite in group:
                if type(sprite) == Player:
                    self.game_constants.surface.blit(sprite.image, sprite.rect.topleft); continue
                self.game_constants.surface.blit(sprite.image, -self.game_constants.offset + sprite.rect.topleft)
        pygame.draw.rect(self.game_constants.surface, (0xFF, 0xFF, 0xFF), self.game_constants.camera_rect, width=3)

    def main(self) -> None:
        pygame.init()
        self.at_startup()
        self.game_constants.is_open = True
        while self.game_constants.is_open:
            self.game_constants.clock.tick()
            self.update()
            pygame.display.flip()
            for event in pygame.event.get():
                self.event_subject.notify(event, self.game_constants)


if __name__ == "__main__":
    LabGameEngine(gameConsts.LabGameConstants(), Event.EventSubject(custom_event_dict)).main()
