import pygame
import numpy as np
import alive_progress
from typing import Any
from icecream import ic
from laby_generator import generate_lab, close_points, is_inside


class Game:pass
game = Game()
pygame.init()
SCREEN_RES = (640, 480)
image = pygame.display.set_mode(SCREEN_RES)
image.fill([0, 0, 0])
pygame.display.set_caption("labyrinthe")

LAB_SHAPE = np.array([5, 5], dtype=object)
labyrinth = generate_lab(tuple(LAB_SHAPE), easy_bt=False)

BORDER_WIDTH: int = 10
POINT_WIDTH: int = 4 * BORDER_WIDTH
LAB_SIZE = LAB_SHAPE * POINT_WIDTH + ((LAB_SHAPE - 1) * BORDER_WIDTH)
START_POINT_COLOR = (255, 0, 0)
EXIT_COLOR = (0, 255, 0)
CENTER = [SCREEN_RES[0] // 2, SCREEN_RES[1] // 2]
OFFSET = CENTER.copy()
LAB_RECT = pygame.Rect(OFFSET, LAB_SIZE)

lab_array = np.zeros((LAB_SHAPE[1], LAB_SHAPE[0]), dtype="int16")
cells_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

for index, value in enumerate(labyrinth):
    lab_array[value[1], value[0]] = index

game.pressed_keys: dict = {}
type coordinate = list[int] | tuple[int]
print(f"{lab_array}\n")


class Cell(pygame.sprite.Sprite):
    def __init__(self, lab: np.ndarray, index: int, pos: coordinate = [0, 0], color=[255, 255, 255]) -> None:
        super().__init__()
        self.image = pygame.Surface([POINT_WIDTH, POINT_WIDTH])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.lab = lab
        self.index = index
        self.arr_index = list(reversed(labyrinth[self.index]))
        self.fixed_x = self.rect.x
        self.fixed_y = self.rect.y

    def adjacent_indexes(self) -> list[int]:
        return [int(lab_array[*i]) for i in close_points(self.arr_index) if is_inside(i, [0, 0], LAB_SHAPE)]
    
    def relative_postion(self, other) -> str:
        """
        relative postion of a cell to self (left, right, up, down)
        """
        y_distance = self.lab[self.index][1] - other.lab[other.index][1]
        x_distance = self.lab[self.index][0] - other.lab[other.index][0]
        if x_distance > 0: return "left"
        if x_distance < 0: return "right"
        if y_distance > 0: return "up"
        if y_distance < 0: return "down"
        return ""
    
    def choose_resize_direction(self) -> str:
        _possible_indexes = [i for i in self.adjacent_indexes() if i < self.index]
        if self.index == 0 or _possible_indexes == []: 
            return ""
        
        _previous: Cell = self.copy()
        _previous.index = max(_possible_indexes)

        return self.relative_postion(_previous)
    
    def copy(self):
        return Cell(self.lab, self.index, self.rect.topleft, self.color)

    def resize(self, color=None) -> None:
        x, y = self.rect.topleft
        rel_pos = self.choose_resize_direction()
        if rel_pos in ("left", "right"):
            self.image = pygame.Surface([POINT_WIDTH + BORDER_WIDTH, POINT_WIDTH])
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "left":    
                self.rect.move_ip(-BORDER_WIDTH, 0)
        
        elif rel_pos in ("up", "down"): 
            self.image = pygame.Surface([POINT_WIDTH, POINT_WIDTH + BORDER_WIDTH])
            self.rect = self.image.get_rect(topleft=[x, y])
            if rel_pos == "up":
                self.rect.move_ip(0, -BORDER_WIDTH)
        self.image.fill(self.color if color == None else color)
        self.fixed_x = self.rect.x
        self.fixed_y = self.rect.y

    def update(self) -> None:
        self.rect.topleft = [self.fixed_x + OFFSET[0], self.fixed_y + OFFSET[1]]


class Player(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group ,rect_args: dict = {}, inital_cell_index: int = 0) -> None:
        super().__init__(group)
        self.image = pygame.image.load("../assets/player.png").convert_alpha()
        self.rect = self.image.get_rect(**rect_args)
        self.speed = 1
        self.cell_index = inital_cell_index
        self.cell_pos_index = labyrinth[self.cell_index]
    
    def move_up(self):
        try:
            self.rect.center = cells_group[lab_array[self.a]]
        except IndexError:
            return
        else:
            OFFSET[1] += self.speed
    
    def move_down(self):
        OFFSET[1] -= self.speed
    
    def move_left(self):
        OFFSET[0] += self.speed
    
    def move_right(self):
        OFFSET[0] -= self.speed

    def move(self) -> None:
        func_map = {
            26: self.move_up, #Z
            4:  self.move_left, #Q
            22: self.move_down, #S
            7:  self.move_right, #D
            43: self.replace, #tab je crois je sais plus
        }
        for key, value in game.pressed_keys.items():
            collisions = pygame.sprite.groupcollide(player_group, cells_group, False, False)
            if key in func_map and value is True and collisions:
                func_map[key]()
                #self.replace(collisions[self])
                break
    
    def update(self) -> None:
        self.move()
        
    def replace(self, cells_collisions: list[Cell] = []) -> bool:
        global OFFSET
        x_coor, y_coor = OFFSET
        x_off, y_off = OFFSET
        x_center, y_center = CENTER
        x_border, y_border = CENTER - LAB_SIZE + self.rect.size
        has_changed = False
        
        if x_off > x_center:#si on est a gauche du plan
            x_coor = x_center; has_changed = True
        if y_off > y_center:#si on est en haut
            y_coor = y_center; has_changed = True
        
        if x_off < x_border:#si on est à droite
            x_coor = x_border; has_changed = True
        if y_off < y_border:#si on est à droite
            y_coor = y_border; has_changed = True
        
        if cells_collisions != []:
            has_changed = has_changed or self.replace_within_cells(cells_collisions)

        OFFSET = [x_coor, y_coor]
        return has_changed
    
    def replace_within_cells(self, cells_collisions: list[Cell]) -> bool:
        if len(cells_collisions) < 2:return False
        cell_1, cell_2 = cells_collisions[0], cells_collisions[1]

        print(cell_1.index < cell_2.index, cells_collisions if len(cells_collisions) > 2 else "")




def draw_laby(group: pygame.sprite.Group, lab: np.ndarray):
    global player
    colors_dict: dict = {
        (0, 0): START_POINT_COLOR,
        tuple(labyrinth[-1]): EXIT_COLOR
    }
    with alive_progress.alive_bar(lab.shape[0], title="PLacement du labyrinthe") as progress_bar:
        for index, value in enumerate(lab):
            cell = Cell(lab=lab, index=index, pos=(value * POINT_WIDTH + (value * BORDER_WIDTH)))
            cell.resize(color=colors_dict.get(tuple(value), None))
            group.add(cell)
            progress_bar()
    player = Player(player_group, {"topleft": OFFSET})


def group_draw(*groups: tuple[pygame.sprite.Group]) -> None:
    for group in groups:
        group.update()
        group.draw(image)


def frame_routine() -> None:
    global OFFSET
    pygame.display.flip()
    pygame.draw.rect(image, [0, 0, 0], image.get_rect())
    group_draw(cells_group, player_group)


def at_startup() -> None:
    draw_laby(cells_group, labyrinth)

def mainloop() -> None:
    is_open = True
    at_startup()
    while is_open:
        frame_routine()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                is_open = False
            
            if event.type == pygame.KEYDOWN:
                game.pressed_keys[event.scancode] = True
                #print(event.scancode)
                if event.scancode == 43:
                    print(OFFSET, CENTER, player.rect.size, LAB_SIZE)
            
            if event.type == pygame.KEYUP:
                game.pressed_keys[event.scancode] = False


if __name__ == "__main__":
    mainloop()