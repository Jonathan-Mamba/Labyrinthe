import pygame
import numpy as np
import typing


def get_image(sprite_sheet: pygame.Surface,
              index: typing.Sequence[int],
              size: typing.Sequence[int],
              scale_factor: float = 1,
              margin: int = 1,
              color: pygame.Color = pygame.Color(0, 0, 0),
              ) -> pygame.Surface:
    image = pygame.Surface(size).convert_alpha()
    image.blit(sprite_sheet, (0, 0), (np.array(index) * np.array(size) + np.array(index) * margin, size))
    image = pygame.transform.scale_by(image, scale_factor)
    image.set_colorkey(color)
    return image
