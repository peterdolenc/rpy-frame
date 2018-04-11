import pygame
from typing import List, Tuple


class BackgroundHelper:

    def __init__(self, display_mode: List[int]):
        self.display_mode = display_mode

    def get_dominant_color_fill(self, colors: List[Tuple[int]]) -> pygame.Surface:
        surface = pygame.Surface(self.display_mode)
        surface.fill(colors[0])
        return surface
