"""
note pour le moi du lendemain: ce fichier est ultra lent sa mère jsp pk(c'esr à cause du not in)
"""

import json
import random

import icecream
import numpy as np
import alive_progress
from typing import Any
from colorama import Fore

type point = list[int] | np.ndarray[int]


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


def is_inside(_point: point, topleft: point, bottomright: point) -> bool:
    return topleft[0] <= _point[0] < bottomright[0] and topleft[1] <= _point[1] < bottomright[1]


def next_possible_points(point_list: np.ndarray[int], points_dict: dict[tuple[int], bool], topleft: point, bottomright: point, index: int = 1) -> list[int]:
    possible_points = []
    for i in close_points(point_list[-index]):
        if is_inside(i, topleft, bottomright) and not points_dict.get(tuple(i), False):
            possible_points.append(i)
    return possible_points


_backtrack_count = 0


def choose_next_point(point_list: np.ndarray[int], points_dict: dict[tuple[int], bool],  size: list) -> point:
    global _backtrack_count
    next_points: list = next_possible_points(point_list, points_dict, [0, 0], size)
    backtrack = 1

    while next_points == []:  #si il y a aucun point disponible
        backtrack += 1
        _backtrack_count += 1
        next_points = next_possible_points(point_list, points_dict, [0, 0], size, backtrack)

    return random.choice(next_points)


def generate_lab(size: point, start_point=None, progress_bar: bool = False) -> np.ndarray[int]:
    """
    retourne une liste de coordonnées qui permet de générer un labyrinthe dans un repère avec [0, 0] le point le plus en haut à gauche du plan.
    """
    if start_point is None:
        start_point = [0, 0]

    AREA = size[0] * size[1]
    point_list: np.ndarray[int] = np.zeros(size)
    points_dict: dict[tuple[int], bool] = {}
    if progress_bar:
        with alive_progress.alive_bar(AREA, title="Génération du plan du labyrinthe") as bar:
            bar()
            for _ in range(AREA - 1):
                next_point = choose_next_point(point_list, points_dict, size)
                point_list = np.append(point_list, [next_point], axis=0)
                points_dict[tuple(next_point)] = True
                bar()
    else:
        for _ in range(AREA - 1):
            next_point = choose_next_point(size)
            point_list = np.append(point_list, [next_point], axis=0)
            points_dict[tuple(next_point)] = True

    return point_list


def main() -> None:
    with open("../../assets/settings.json", "r") as f:
        settings = json.loads(f.read())
        SIZE = [settings["labyrinthe.taille"][0], settings["labyrinthe.taille"][1]]
    laby = generate_lab(SIZE, start_point=settings["start_point"])

    log(title="liste de la bonne taille", data=len(laby) == SIZE[0] * SIZE[1], other=f"{len(laby):,}")
    log("backtrack", _backtrack_count > 0, f"{_backtrack_count:,}")

    with open("../../assets/output.json", "w") as f:
        f.write(json.dumps({"liste_coor": "ouias bah ca merche pas"}))


if __name__ == '__main__':
    main()
