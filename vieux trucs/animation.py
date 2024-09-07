import itertools
import os
import sys
import time
import icecream
import numpy as np
from colorama import Fore, init

sys.path.append(r"C:\Users\jojod\Bureau\fichiers_python\autres\labyrinthe")
from util.laby_generator import close_points, LabWalker

init(True)


class TerminalRenderer:
    frame_sleep_time: float = .1
    content: np.ndarray[str]
    blank: str = f"{Fore.LIGHTBLACK_EX}*"

    @classmethod
    def render(cls):
        print("\n".join([
            "".join(sub_array) for sub_array in cls.content
        ]))
        time.sleep(TerminalRenderer.frame_sleep_time)

    @classmethod
    def set_char(cls, index, char: str):
        cls.content[index[0], index[1]] = char + " "

    @classmethod
    def fill(cls, size, char=None):
        char = cls.blank if char is None else char
        char += " "
        cls.content = np.full(size, char)


def rel_pos(_point: np.ndarray, other: np.ndarray):
    """
    other is to the {return value} of point
    """
    x, y = _point - other
    if x > 0: return "left"
    if x < 0: return "right"
    if y > 0: return "up"
    if y < 0: return "down"
    return ""


def get_char(_point: np.ndarray, _previous_point: np.ndarray, _next_point: np.ndarray) -> str:
    prev_to_curr: str = rel_pos(_point, _previous_point)
    curr_to_next: str = rel_pos(_next_point, _point)
    if prev_to_curr == curr_to_next:
        _rel_pos = curr_to_next
        if _rel_pos == "left" or _rel_pos == "right": return "─"
        if _rel_pos == "up" or _rel_pos == "down": return "|"

    elif curr_to_next == "left" and prev_to_curr == "up": return "└"
    elif curr_to_next == "left" and prev_to_curr == "down": return "┌"
    elif curr_to_next == "right" and prev_to_curr == "up": return "┘"
    elif curr_to_next == "right" and prev_to_curr == "down": return "┐"
    else:
        return "x"



class PointCreationObserver:
    def __init__(self):
        self.index: int = -1
        self.color = Fore.RED
        self.colors = itertools.cycle([Fore.MAGENTA, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.RED])
        self.next_point = np.array([0, 0])
        self.previous_point = np.array([0, 0])
        self.current_point = np.array([0, 0])

    def notify(self, point: np.ndarray[int]) -> None:
        os.system("cls")
        self.index += 1
        self.previous_point = self.current_point.copy()
        self.current_point = self.next_point.copy()
        self.next_point = point.copy()

        if [self.previous_point[0], self.previous_point[1]] not in close_points(point):
            self.color = self.colors.__next__()

        if self.index > 1:
            TerminalRenderer.set_char(self.current_point,
                                      f"{self.color}{get_char(self.current_point, self.previous_point, self.next_point)}")
            TerminalRenderer.render()





def to_lab_array(point_list: np.ndarray[int], lab_shape: np.ndarray) -> np.ndarray[int]:
    lab_array: np.ndarray[int] = np.zeros(list(reversed(lab_shape)), dtype=np.int8)
    for index, value in enumerate(point_list):
        lab_array[value[1], value[0]] = index
    return lab_array


def main():
    LAB_SIZE = [
        9, 9  #int(input("l: ")),
        #int(input("L: "))
    ]
    TerminalRenderer.fill(LAB_SIZE)

    walker: LabWalker = LabWalker(np.array([[0, 0]]), [0, 0], PointCreationObserver().notify)
    walker.generate(LAB_SIZE)
    print((to_lab_array(walker.point_list, LAB_SIZE)))


if __name__ == "__main__":
    main()
