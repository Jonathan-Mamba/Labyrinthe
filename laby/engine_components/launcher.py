import numpy as np
import pygame
import icecream
from typing import Callable, Iterable
from laby.constants import LabEngineConstants, LabGameConstants
from laby.event.custom import CustomEvent
from laby.util.laby_generator import is_inside, close_points
from laby.sprite import Cell, Wall, Junction
from laby.sprite.entity import Player
from laby.util import tools
from laby.util.misc import Direction


class Launcher:
    """
    Singleton object responsible for all the tasks at startup
    """

    def __init__(self, gc: LabGameConstants, ec: LabEngineConstants):
        self.game_constants = gc
        self.engine_constants = ec
        self.is_inside_lab: Callable[[Iterable[int | float]], bool] = lambda x: is_inside(x, (0, 0), gc.LAB_SHAPE)

    def start(self):
        self.engine_constants.surface = pygame.display.set_mode(self.game_constants.SCREEN_RES, pygame.RESIZABLE)
        pygame.display.set_caption(self.engine_constants.title)

        pygame.time.set_timer(CustomEvent.PLAYER_IDLE, 80)

        self.engine_constants.camera_rect = pygame.Rect(
            [self.game_constants.CAMERABOX_OFFSET, self.game_constants.CAMERABOX_OFFSET],
            self.game_constants.SCREEN_RES - (self.game_constants.CAMERABOX_OFFSET * 2)
        )

        # TODO: why not generate a "WorldMap" image at startup instead of recreating it at each frame ?
        self.create_cells()
        self.create_junctions()
        self.create_walls()

        self.engine_constants.player_group.sprite = Player(self.engine_constants.cells_group.sprites()[0].rect.center)
        self.engine_constants.last_cell = self.engine_constants.cells_group.sprites()[-1]
        self.engine_constants.last_cell.image.fill(pygame.Color("white"))

    def create_cells(self) -> None:
        lab_array = self.game_constants.lab_array
        for index, value in enumerate(self.game_constants.labyrinth):
            cell = Cell(index, value * self.game_constants.CELL_WIDTH + (value * self.game_constants.BORDER_WIDTH))
            self.engine_constants.cells_group.add(cell)
            cell.set_color()

            # filling cell.edges
            adjacent_cells = [i for i in close_points(self.game_constants.labyrinth[cell.index])
                              if self.is_inside_lab(i)]
            max_index: int = -1
            for point in adjacent_cells:
                # if point is right next or right before cell in order:
                if abs(lab_array.get(point) - cell.index) == 1:
                    cell.edges.add((
                        tools.get_relative_position(cell.arr_index, point),
                        lab_array.get(point) < cell.index
                    ))
                # if cell starts a new branch and max_index < lab_array[point] < cell.index
                elif cell.index in self.game_constants.branch_array and max_index < lab_array.get(point) < cell.index:
                    max_index = lab_array.get(point)
            if max_index != -1 and cell.index != 0:
                cell.edges.add(
                    (tools.get_relative_position(cell.arr_index, self.game_constants.labyrinth[max_index]), True))

    def create_junctions(self) -> None:
        cells: list[Cell] = self.engine_constants.cells_group.sprites()
        for cell in cells:
            for direction, is_before in cell.edges:
                if is_before:
                    junction_topleft = cell.rect.topleft
                    if direction == Direction.NORTH:
                        junction_topleft = cell.rect.topleft - pygame.Vector2(0, self.game_constants.BORDER_WIDTH)
                    elif direction == Direction.SOUTH:
                        junction_topleft = cell.rect.bottomleft
                    elif direction == Direction.WEST:
                        junction_topleft = cell.rect.topleft - pygame.Vector2(self.game_constants.BORDER_WIDTH, 0)
                    elif direction == Direction.EAST:
                        junction_topleft = cell.rect.topright

                    Junction(
                        self.game_constants.CELL_WIDTH,
                        self.game_constants.BORDER_WIDTH,
                        cell.color,
                        direction in (Direction.NORTH, Direction.SOUTH),
                        junction_topleft,
                        self.engine_constants.junction_group
                    )

    def create_walls(self):
        # TODO: will merge all of the walls into one giant sprite or all of the straight lines
        cells: list[Cell] = self.engine_constants.cells_group.sprites()
        lab_array = self.game_constants.lab_array
        image_size = (self.game_constants.CELL_WIDTH, self.game_constants.CELL_WIDTH)
        for cell in cells:
            edges: list[Direction] = list(cell.direction_edges)
            adjacent_branch_cells = [
                point for point in close_points(cell.arr_index)
                if self.is_inside_lab(point)
                if lab_array.get(point) in self.game_constants.branch_array  # AND
                if lab_array.get(point) > cell.index  # AND
                if tools.get_relative_position(point, cell.arr_index) in cells[lab_array.get(point)].direction_edges
            ]

            if not edges:
                Wall.from_zero(cell.rect.topleft, image_size, self.engine_constants.wall_group)
                continue

            if len(adjacent_branch_cells) == 1:
                max_index: int = 0
                # les cellules qui se trouvent après cell dans l'ordre et a coté de adjacent_branch_cell
                for point in close_points(adjacent_branch_cells[0]):
                    # max_index < lab_array[point] < lab_array[adjacent_branch_cell]
                    if self.is_inside_lab(point) and max_index < lab_array.get(point) < lab_array.get(adjacent_branch_cells[0]):
                        max_index = lab_array.get(point)

                if max_index == cell.index:
                    edges.append(tools.get_relative_position(cell.arr_index, adjacent_branch_cells[0]))

            if len(adjacent_branch_cells) == 2:
                Wall.from_four(cell.rect.topleft, image_size, self.engine_constants.wall_group)
                continue

            if len(edges) == 1:
                Wall.from_one(cell.rect.topleft, image_size, edges[0], self.engine_constants.wall_group)
            elif len(edges) == 2:
                Wall.from_two(cell.rect.topleft, image_size, edges[1], edges[0], self.engine_constants.wall_group)
            elif len(edges) == 3:
                direction: int = [i for i in (0, 2, 4, 6) if i not in edges][0]  # y'en a qu'un
                Wall.from_three(cell.rect.topleft, image_size, direction, self.engine_constants.wall_group)
