import pygame as pg
import numpy as np
import typing


def get_image(spritesheet: pg.Surface,
              index: typing.Sequence[int],
              size: typing.Sequence[int],
              scale_factor: float = 1,
              color: pg.Color = pg.Color(0, 0, 0),
              ) -> pg.Surface:
    image = pg.Surface(size).convert_alpha()
    image.blit(spritesheet, (0, 0), (np.array(index) * np.array(size), size))
    image = pg.transform.scale_by(image, scale_factor)
    image.set_colorkey(color)
    return image
