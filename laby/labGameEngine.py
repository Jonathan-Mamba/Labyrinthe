import pygame
import icecream
import numpy as np
from laby.event import EventSubject, EventObserver
from laby.constants import LabGameConstants, LabEngineConstants
from laby.event.custom import custom_event_dict, CustomEvent
from laby.util.tools import Direction
from laby.engine_components import Launcher, EngineObserver, Renderer


class LabGameEngine:
    def __init__(self) -> None:
        pygame.init()
        # None of these are private bc there is and should be NO reference to LabGameEngine
        self.game_constants: LabGameConstants = LabGameConstants()
        self.engine_constants: LabEngineConstants = LabEngineConstants()
        self.event_subject: EventSubject = EventSubject(custom_event_dict)

        self.launcher: Launcher = Launcher(self.game_constants, self.engine_constants)
        self.engine_observer: EngineObserver = EngineObserver(self.engine_constants)
        self.renderer: Renderer = Renderer()

    def at_startup(self) -> None:
        self.launcher.start()
        del self.launcher  # like I said, only ONE use

        x = (
            (self.engine_observer.event_quit, pygame.QUIT),
            (self.engine_observer.video_resize, pygame.VIDEORESIZE),
            (self.engine_observer.debug, pygame.KEYDOWN),
            (self.engine_constants.player.animate, CustomEvent.PLAYER_IDLE)
        )
        for func, event_type in x:
            self.event_subject.add_observer(EventObserver(func), event_type)

    def process_movement(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_q]:
            self.engine_constants.player.velocity.x -= 1
            self.engine_constants.player.set_direction(Direction.WEST)

        elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.engine_constants.player.velocity.x += 1
            self.engine_constants.player.set_direction(Direction.EAST)

        elif pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_z]:
            self.engine_constants.player.velocity.y -= 1
            self.engine_constants.player.set_direction(Direction.NORTH)

        elif pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.engine_constants.player.velocity.y += 1
            self.engine_constants.player.set_direction(Direction.SOUTH)

        self.engine_constants.player.update_velocity()
        player_rect = self.engine_constants.player.rect
        camera_rect = self.engine_constants.camera_rect

        if player_rect.left < camera_rect.left:
            camera_rect.left = player_rect.left
        if player_rect.right > camera_rect.right:
            camera_rect.right = player_rect.right
        if player_rect.bottom > camera_rect.bottom:
            camera_rect.bottom = player_rect.bottom
        if player_rect.top < camera_rect.top:
            camera_rect.top = player_rect.top

        self.engine_constants.offset = np.array(camera_rect.topleft) - self.game_constants.CAMERABOX_OFFSET

    def update(self) -> None:
        self.process_movement()
        for group in self.engine_constants.groups:
            if group == self.engine_constants.player_group:
                self.engine_constants.player.update(wall_group=self.engine_constants.wall_group, junction_group=self.engine_constants.junction_group)
                continue
            group.update()
        self.renderer.render(self.game_constants, self.engine_constants)

    def main(self) -> None:
        self.at_startup()
        self.engine_constants.is_open = True
        while self.engine_constants.is_open:
            self.update()
            self.engine_constants.clock.tick(self.game_constants.FRAMERATE)
            pygame.display.flip()
            for event in pygame.event.get():
                self.event_subject.notify(event)


if __name__ == "__main__":
    LabGameEngine().main()
