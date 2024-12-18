from laby.sprite import LabSprite


class Entity(LabSprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._health: float = 10

    def get_health(self) -> float:
        return self._health

    def set_health(self, value: float) -> None:
        self._health = value
