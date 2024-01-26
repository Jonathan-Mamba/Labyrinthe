

"""
note pour le moi du lendemain: problème avec la recursion qui fait que le walker reste au même endroit pendant le backtrack
 est causé par le fait que le point qui oblige le backtracking est supprimé de la point list pendant celui-ci
 solution possible: une while loop pcq la récursion c pas fou
"""

import os
import json
import random
import alive_progress
from typing import Any
from icecream import ic
from colorama import Fore, init
init(autoreset=True)

type point = list[int, int]

def log(title: str, data: Any, other: Any = ""):
    _str = f"{Fore.LIGHTBLACK_EX}{title}{Fore.WHITE}: {Fore.BLUE}{data}"
    print(f"{_str}{Fore.RESET}" if other == '' else f"{_str} {Fore.WHITE}| {Fore.GREEN}{other}{Fore.RESET}")


def close_points(_point: point) -> list:
    x, y = _point
    return [
        [x - 1, y],
        [x + 1, y],
        [x, y + 1],
        [x, y - 1],
    ]


def is_inside(_point: point, topleft: point, bottomright: point) -> bool:
    return topleft[0] <= _point[0] < bottomright[0] and topleft[1] <= _point[1] < bottomright[1]


def find_next_points(point_list: list, topleft: point, bottomright: point, pointer: int = 1):
    possible_points = []
    for i in close_points(point_list[-pointer]):
        if is_inside(i, topleft=[0, 0], bottomright=bottomright) and i not in point_list:
            possible_points.append(i)
    return possible_points


_backtrack_count = 0
def calculate_next_point(point_list: list, size: list):
    global _backtrack_count
    next_points = find_next_points(point_list, [0, 0], bottomright=size)
    backtrack = 1
    while next_points == []:#si il y a aucun point disponible
        _backtrack_count += 1
        backtrack += 1
        next_points = find_next_points(point_list, [0, 0], bottomright=size, pointer=backtrack)                              
    return random.choice(next_points)


def generate_lab(size: list[int, int], start_point: point = [0, 0]) -> list:
    point_list = [start_point]
    AREA = size[0] * size[1]
    with alive_progress.alive_bar(AREA) as bar:
        for i in range(1, AREA):
            point_list.append(calculate_next_point(point_list, size))
            bar()
        bar()
    return point_list


def error(a: Any) -> None:
    print(f"{Fore.YELLOW}{a}")

def style_input(a: str) -> str:
    return input(f"{Fore.LIGHTBLACK_EX}{a}{Fore.WHITE}: {Fore.BLUE}")



def main() -> None:
    SIZE = [
        int(style_input("Largeur")), 
        int(style_input("Hauteur")),
        ]
    
    laby = generate_lab(SIZE)
    
    log(title="liste de la bonne taille", data=len(laby) == SIZE[0] * SIZE[1], other=len(laby))
    log("backtrack", _backtrack_count > 0, _backtrack_count)
    
    with open("output.json", "w") as f:
        f.write(json.dumps({"liste_coor":laby}))


if __name__ == '__main__':
    main()