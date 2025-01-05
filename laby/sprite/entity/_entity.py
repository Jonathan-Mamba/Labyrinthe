from laby.sprite import LabSprite


class Entity(LabSprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._health: float = 10

    @property
    def health(self) -> float: return self._health

    @health.setter
    def health(self, value: float): self._health = value
