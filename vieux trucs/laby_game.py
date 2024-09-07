import pygame
import numpy as np
from labyrinthe.GameCore.Cell import Cell
from util.laby_generator import generate_lab


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.SCREEN_RES = np.array([640, 480])
        self.LAB_SIZE = np.array([10, 10], dtype="int8")
        self.BORDER_WIDTH = 8
        self.CELL_WIDTH = 4 * self.BORDER_WIDTH
        self.EXIT_COLOR = pygame.color.Color((0, 255, 0))

        self.labyrinth = generate_lab([int(self.LAB_SIZE[0]), int(self.LAB_SIZE[1])])
        self.lab_array = np.zeros((self.LAB_SIZE[1], self.LAB_SIZE[0]), dtype="int16")
        self.offset = self.SCREEN_RES // 2
        self.pressed_keys: dict = {}

        self.EXIT = self.labyrinth[-1]
        self.LAB_RECT = pygame.Rect(self.offset,
                                    self.LAB_SIZE * self.CELL_WIDTH + ((self.LAB_SIZE - 1) * self.BORDER_WIDTH))
        self.surface = pygame.display.set_mode(self.SCREEN_RES)
        pygame.display.set_caption("Labyrinthe")

        self.cells_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.groups: list[pygame.sprite.Group] = [self.player_group, self.cells_group]

        for index, value in enumerate(self.labyrinth):
            self.lab_array[value[1], value[0]] = index

    def create_cells(self) -> None:
        for index, value in enumerate(self.labyrinth):
            #ic(index, value)
            cell = Cell(game=self, index=index, pos=(value * self.CELL_WIDTH + (value * self.BORDER_WIDTH)))
            cell.align_to_previous()
            self.cells_group.add(cell)

    def update(self) -> None:
        self.groups = [
            self.cells_group,
        ]

    def at_startup(self) -> None:
        print(self.lab_array)
        self.create_cells()

    def group_draw(self):
        for group in self.groups:
            group.update()
            group.draw(self.surface)

    def frame_routine(self) -> None:
        self.update()
        self.group_draw()

    def gameloop(self) -> None:
        is_open = True
        self.at_startup()
        while is_open:
            self.frame_routine()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    is_open = False
                    break


def main() -> None:
    pygame.init()
    game = Game()
    game.gameloop()


if __name__ == "__main__":
    main()
