import random
import numpy as np
import alive_progress
from typing import Any
from colorama import Fore
type point = list[int] | np.ndarray[Any, int] | tuple[int, int]


def log(title: str, data: Any, other: Any = "") -> None:
    _str = f"{Fore.LIGHTBLACK_EX}{title}{Fore.WHITE}: {Fore.BLUE}{data}"
    print(f"{_str}{Fore.RESET}" if other == '' else f"{_str} {Fore.WHITE}| {Fore.GREEN}{other}{Fore.RESET}")


def close_points(_point: point) -> list:
    x, y = _point[0], _point[1]
    return [
        [x - 1, y],
        [x + 1, y],
        [x, y + 1],
        [x, y - 1],
    ]

# oui cette classe sert a rien mais si je l'enlève ca marche plus
class LabWalker:
    def __init__(self, point_list: np.ndarray[Any, int], start_point: point, func=lambda x: None) -> None:
        self.point_list = point_list
        self.start_point = start_point
        self.points_dict = {tuple(start_point): True}
        self.func = func


def is_inside(_point: point, topleft: point, bottomright: point) -> bool:
    return topleft[0] <= _point[0] < bottomright[0] and topleft[1] <= _point[1] < bottomright[1]


def next_possible_points(walker: LabWalker, topleft: point, bottomright: point, index: int = 1) -> list[int]:
    possible_points = []
    for i in close_points(walker.point_list[-index]):
        if is_inside(i, topleft=topleft, bottomright=bottomright) and not walker.points_dict.get(tuple(i), False):
            possible_points.append(i)
    return possible_points


def choose_next_point(walker: LabWalker, size: list) -> point:
    next_points: list = next_possible_points(walker, [0, 0], bottomright=size)
    backtrack = 1

    while not next_points:  # si il y a aucun point disponible
        backtrack += 1
        next_points = next_possible_points(walker, [0, 0], bottomright=size, index=backtrack)

    return random.choice(next_points)


def generate_lab(size: point, start_point=None, progress_bar: bool = False) -> np.ndarray[Any, int]:
    """
    retourne une liste de coordonnées qui permet de générer un labyrinthe dans un repère avec [0, 0] le point le plus en haut à gauche du plan.
    """
    if start_point is None:
        start_point = [0, 0]

    walker: LabWalker = LabWalker(point_list=np.array([start_point], dtype="int16"), start_point=start_point)
    AREA = size[0] * size[1]
    if progress_bar:
        with alive_progress.alive_bar(AREA, title="Génération du plan du labyrinthe") as bar:
            bar()
            for _ in range(AREA - 1):
                next_point = choose_next_point(walker, size)
                walker.point_list = np.append(walker.point_list, [next_point], axis=0)
                walker.points_dict[tuple(next_point)] = True
                bar()
    else:
        for _ in range(AREA - 1):
            next_point = choose_next_point(walker, size)
            walker.point_list = np.append(walker.point_list, [next_point], axis=0)
            walker.points_dict[tuple(next_point)] = True

    return walker.point_list
