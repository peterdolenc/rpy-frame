from __future__ import division
import pygame
from typing import List, Tuple

from pattern_generator import PatternGenerator


class BackgroundHelper:

    def __init__(self, display_mode: List[int]):
        self.display_mode = display_mode
        self.pattern_generator = PatternGenerator(display_mode)

    @staticmethod
    def to_hex(rgb):
        rgb = tuple([int(rgb[i]) for i in range(0, len(rgb))])
        return '#%02x%02x%02x' % rgb

    def get_dominant_color_fill(self, colors: List[Tuple[int]]) -> pygame.Surface:
        surface = pygame.Surface(self.display_mode)
        surface.fill(colors[0])
        return surface

    def get_dominant_pattern(self, colors: List[Tuple[int]]) -> pygame.Surface:
        hex_colors = (self.to_hex(c) for c in colors[:5])
        surface = self.pattern_generator.playful_circles(*hex_colors)

        return surface


