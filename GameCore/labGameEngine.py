import numpy as np
import icecream
from GameCore.event import Event, Observers
from GameCore import labGameConstants as gameConsts
from GameCore.sprite.cell import Cell
from GameCore.sprite.player import Player
from GameCore.sprite.wall import Wall
from GameCore.event.custom import custom_event_dict, CustomEvent
from GameCore.util.laby_generator import close_points, is_inside
from GameCore.util.misc import Direction
from GameCore.util import tools
import pygame


class LabGameEngine:
    def __init__(self, game_constants: gameConsts.LabGameConstants, engine_constants: gameConsts.LabEngineConstants,
                 event_subject: Event.EventSubject) -> None:
        self.game_constants: gameConsts.LabGameConstants = game_constants
        self.engine_constants: gameConsts.LabEngineConstants = engine_constants  # if it could this would be private
        self.event_subject: Event.EventSubject = event_subject

    def set_timers(self) -> None:
        pygame.time.set_timer(pygame.event.Event(CustomEvent.PLAYER_IDLE.value), 80)

    def at_startup(self) -> None:
        self.engine_constants.surface = pygame.display.set_mode(self.game_constants.SCREEN_RES, pygame.RESIZABLE)
        pygame.display.set_caption(self.engine_constants.title)

        self.set_timers()
        self.create_cells()
        self.create_walls()
        self.add_observers()

        self.engine_constants.player_group.sprite = Player(self.engine_constants.cells_group.sprites()[0].rect.center)
        self.engine_constants.camera_rect = pygame.Rect(
            [self.game_constants.CAMERABOX_OFFSET, self.game_constants.CAMERABOX_OFFSET],
            self.game_constants.SCREEN_RES - (self.game_constants.CAMERABOX_OFFSET * 2)
        )

    def create_cells(self) -> None:
        for index, value in enumerate(self.game_constants.labyrinth):
            cell = Cell(self.game_constants.CELL_WIDTH, self.game_constants.labyrinth, index=index,
                        pos=(value * self.game_constants.CELL_WIDTH + (value * self.game_constants.BORDER_WIDTH)))
            cell.align_to_previous(self.game_constants)
            self.engine_constants.cells_group.add(cell)

    def create_walls(self) -> None:
        for var in self.engine_constants.cells_group:
            cell: Cell = var
            directions: np.ndarray = np.array([])
            # write it down on a piece of paper (I know this looks bad)
            for i in close_points(self.game_constants.labyrinth[cell.index]):
                # if i is in labyrinth:
                if is_inside(i, (0, 0), self.game_constants.LAB_SIZE):
                    # if i is right next or right before cell in order:
                    if abs(self.game_constants.lab_array[*reversed(i)] - cell.index) <= 1:
                        directions = np.append(directions, tools.get_relative_postion(tuple(reversed(cell.arr_index)), i))

                    # if cell marks a new branch and cell is after i:
                    elif cell.index in self.game_constants.branch_array and (
                            cell.index > self.game_constants.lab_array[*reversed(i)]):
                        directions = np.append(directions, tools.get_relative_postion(tuple(reversed(cell.arr_index)), i))

            if directions.size == 0:
                continue
            elif directions.size == 1:
                self.engine_constants.walls_group.add(Wall(cell.rect.topleft, 1, directions[0], cell.rect.size))
            elif directions.size == 2:
                continue
            elif directions.size == 3:
                for i in (0, 2, 4, 6):
                    if i not in directions:
                        self.engine_constants.walls_group.add(
                            Wall(cell.rect.topleft, 3, i, cell.rect.size)
                        )
                        icecream.ic(cell.index)
                        break


    def add_observers(self) -> None:
        self.event_subject.add_observer(Event.EventObserver(Observers.event_quit), pygame.QUIT)
        self.event_subject.add_observer(Event.EventObserver(Observers.debug), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.player_key_down), pygame.KEYDOWN)
        self.event_subject.add_observer(Event.EventObserver(Observers.video_resize), pygame.VIDEORESIZE)
        self.event_subject.add_observer(Event.EventObserver(Observers.player_idle), CustomEvent.PLAYER_IDLE.value)

    def process_movement(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_q]:
            self.engine_constants.player.velocity.x -= 1
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.engine_constants.player.velocity.x += 1
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_z]:
            self.engine_constants.player.velocity.y -= 1
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.engine_constants.player.velocity.y += 1

        try:
            self.engine_constants.player.velocity = (self.engine_constants.player.velocity.normalize() * self.game_constants.SPEED)
        except ValueError:
            pass

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
        pygame.draw.rect(self.engine_constants.surface, [0, 0, 0], pygame.Rect([0, 0], self.game_constants.SCREEN_RES))
        for group in self.engine_constants.groups:
            group.update(self.game_constants)
            for sprite in group:
                self.engine_constants.surface.blit(sprite.image, -self.engine_constants.offset + sprite.rect.topleft)
        pygame.draw.rect(self.engine_constants.surface, [255, 255, 255], pygame.Rect((0, 0), (self.game_constants.WALL_WIDTH, self.game_constants.WALL_WIDTH)), width=3)

    def main(self) -> None:
        pygame.init()
        self.at_startup()
        self.engine_constants.is_open = True
        while self.engine_constants.is_open:
            self.update()
            self.engine_constants.clock.tick(self.game_constants.FRAMERATE)
            pygame.display.flip()
            for event in pygame.event.get():
                self.event_subject.notify(event, self.game_constants, self.engine_constants)


if __name__ == "__main__":
    LabGameEngine(gameConsts.LabGameConstants(), gameConsts.LabEngineConstants(),
                  Event.EventSubject(custom_event_dict)).main()
