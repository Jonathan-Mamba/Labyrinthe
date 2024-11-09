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

    def set_timers(self) -> None:
        pygame.time.set_timer(pygame.event.Event(CustomEvent.PLAYER_IDLE.value), 80)

    def at_startup(self) -> None:
        self.game_constants.surface = pygame.display.set_mode(self.game_constants.SCREEN_RES, pygame.RESIZABLE)
        pygame.display.set_caption(self.game_constants.title)

        self.game_constants.player_group.sprite = Player(self.game_constants.SCREEN_RES / 2)
        self.set_timers()
        self.create_cells()
        self.add_observers()

    def create_cells(self) -> None:
        for index, value in enumerate(self.game_constants.labyrinth):
            cell = Cell(self.game_constants.CELL_WIDTH, self.game_constants.labyrinth, index=index,
                        pos=(value * self.game_constants.CELL_WIDTH + (value * self.game_constants.BORDER_WIDTH)))
            cell.align_to_previous(self.game_constants)
            self.game_constants.cells_group.add(cell)

    def add_observers(self) -> None:
        self.event_subject.add_observer(Event.EventObserver(Observers.event_quit), pygame.QUIT)
        self.event_subject.add_observer(Event.EventObserver(Observers.debug), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.player_key_down), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.video_resize), pygame.VIDEORESIZE)
        self.event_subject.add_observer(Event.EventObserver(Observers.player_idle), CustomEvent.PLAYER_IDLE.value)

    def process_movement(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_q]:
            self.game_constants.player.velocity.x -= 1
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.game_constants.player.velocity.x += 1
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_z]:
            self.game_constants.player.velocity.y -= 1
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.game_constants.player.velocity.y += 1

        try:
            self.game_constants.player.velocity = (self.game_constants.player.velocity.normalize() * self.game_constants.SPEED)
        except ValueError:
            pass

        self.game_constants.player.update_velocity()
        player_rect = self.game_constants.player.rect
        camera_rect = self.game_constants.camera_rect

        if player_rect.left < camera_rect.left:
            camera_rect.left = player_rect.left
        if player_rect.right > camera_rect.right:
            camera_rect.right = player_rect.right
        if player_rect.bottom > camera_rect.bottom:
            camera_rect.bottom = player_rect.bottom
        if player_rect.top < camera_rect.top:
            camera_rect.top = player_rect.top

        self.game_constants.offset = np.array(camera_rect.topleft) - self.game_constants.CAMERABOX_OFFSET

    def update(self) -> None:
        self.process_movement()
        pygame.draw.rect(self.game_constants.surface, [0, 0, 0], pygame.Rect([0, 0], self.game_constants.SCREEN_RES))
        for group in self.game_constants.groups:
            group.update(self.game_constants)
            for sprite in group:
                self.game_constants.surface.blit(sprite.image, -self.game_constants.offset + sprite.rect.topleft)

    def main(self) -> None:
        pygame.init()
        self.at_startup()
        self.game_constants.is_open = True
        while self.game_constants.is_open:
            self.update()
            self.game_constants.clock.tick(120)
            pygame.display.flip()
            for event in pygame.event.get():
                self.event_subject.notify(event, self.game_constants)


if __name__ == "__main__":
    LabGameEngine(gameConsts.LabGameConstants(), Event.EventSubject(custom_event_dict)).main()
