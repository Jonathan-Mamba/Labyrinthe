

"""
note pour le moi du lendemain: ce fichier est ultra lent sa mère jsp pk(c'esr à cause du not in)
"""


import json
import random
import numpy as np
import alive_progress
from typing import Any
from colorama import Fore

type point = list[int, int]

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



class LabWalker:
    def __init__(self, point_list: np.ndarray, start_point: point) -> None:
        self.point_list = point_list
        self.start_point = start_point
        self.points_dict = {tuple(start_point):True}



def is_inside(_point: point, topleft: point, bottomright: point) -> bool:
    return topleft[0] <= _point[0] < bottomright[0] and topleft[1] <= _point[1] < bottomright[1]



def find_next_possible_points(walker: LabWalker, topleft: point, bottomright: point, pointer: int = 1) -> list:
    possible_points = []
    for i in close_points(walker.point_list[-pointer]):
        if is_inside(i, topleft=[0, 0], bottomright=bottomright) and not walker.points_dict.get(tuple(i), False):
            possible_points.append(i)
    return possible_points



_backtrack_count = 0
def choose_next_point(walker: LabWalker, size: list, easy_bt: bool = False) -> point:
    global _backtrack_count
    next_points: list = find_next_possible_points(walker, [0, 0], bottomright=size)
    backtrack = 1
    
    while next_points == []:#si il y a aucun point disponible
        backtrack += 1
        _backtrack_count += 1
        next_points = find_next_possible_points(walker, [0, 0], bottomright=size, pointer=backtrack)
    
    if easy_bt and backtrack > 1:
        walker.point_list = np.append(walker.point_list, [walker.point_list[-backtrack]], axis=0)

    return random.choice(next_points)



def generate_lab(size: point, start_point: point = [0, 0], easy_bt: bool = False) -> np.ndarray:
    """
    retourne une liste de coordonnées qui permet de générer un labyrinthe dans un repère avec [0, 0] le point le plus en haut à gauche du plan.
    """
    walker: LabWalker = LabWalker(point_list=np.array([start_point]), start_point=start_point)
    AREA = size[0] * size[1]
    with alive_progress.alive_bar(AREA, title="Génération du plan du labyrinthe") as bar:    
        bar()
        for _ in range(AREA - 1):
            next_point = choose_next_point(walker, size, easy_bt)
            walker.point_list = np.append(walker.point_list, [next_point], axis=0)
            walker.points_dict[tuple(next_point)] = True
            bar()
    return walker.point_list



def main() -> None:
    with open("assets/settings.json", "r") as f:
        settings = json.loads(f.read())
        SIZE = [settings["labyrinthe.taille"][0], settings["labyrinthe.taille"][1]]
    laby = generate_lab(SIZE, start_point=settings["start_point"])
    
    log(title="liste de la bonne taille", data=len(laby) == SIZE[0] * SIZE[1], other=f"{len(laby):,}")
    log("backtrack", _backtrack_count > 0, f"{_backtrack_count:,}")
    
    with open("assets/output.json", "w") as f:
        f.write(json.dumps({"liste_coor":"ouias bah ca merche pas"}))


if __name__ == '__main__':
    main()