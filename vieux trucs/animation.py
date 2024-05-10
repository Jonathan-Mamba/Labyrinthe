import itertools
import os
import time
import icecream
import numpy as np
from colorama import Fore, init
from laby_generator import LabWalker, close_points

init(True)

color = Fore.RED
colors = itertools.cycle([Fore.MAGENTA, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.RED])
previous_point = [0, 0]


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


def get_char(_point, _previous_point) -> str:
    x, y = _point[0] - _previous_point[0], _point[1] - _previous_point[1]
    if x < 0: return "←"
    if x > 0: return "→"
    if y < 0: return "↑"
    if y > 0: return "↓"
    return "+"


def truc(point):
    global colors, previous_point, color
    if previous_point not in close_points(point):
        color = colors.__next__()
    TerminalRenderer.set_char(list(reversed(point)), f"{color}{get_char(point, previous_point)}")
    os.system("cls")
    diff = np.array(point) - np.array(previous_point)
    icecream.ic(point, previous_point)
    icecream.ic(diff)
    TerminalRenderer.render()
    previous_point = point


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

    walker: LabWalker = LabWalker(np.array([[0, 0]]), [0, 0], truc)
    walker.generate(LAB_SIZE)
    print((to_lab_array(walker.point_list, LAB_SIZE)))


if __name__ == "__main__":
    main()
