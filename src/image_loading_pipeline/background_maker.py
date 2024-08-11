import random

import pygame
from typing import List, Tuple
from image_loading_pipeline.pattern_generator import PatternGenerator
from settings import Settings


class BackgroundMaker:

    def __init__(self, display_mode: List[int], settings: Settings):
        self.display_mode = display_mode
        self.pattern_generator = PatternGenerator(display_mode)
        self.settings = settings

    @staticmethod
    def to_hex(rgb):
        rgb = tuple([int(rgb[i]) for i in range(0, len(rgb))])
        return '#%02x%02x%02x' % rgb

    def get_dominant_color_fill(self, colors: List[Tuple[int]]) -> pygame.Surface:
        surface = pygame.Surface(self.display_mode)
        surface.fill(colors[0])
        return surface.convert()

    def get_dominant_pattern(self, colors: List[Tuple[int]], animation=None) -> pygame.Surface:
        hex_colors = (self.to_hex(c) for c in colors[:5])

        if random.random() > 0.5:
            surface = self.pattern_generator.playful_circles(*hex_colors, animation, self.settings.background_ppi, self.settings.background_alpha, self.settings.background_lightness,
                                                             blur=self.settings.blur_background, blur_radius=self.settings.blur_background_radius*0.75)

        else:
            surface = self.pattern_generator.astro_stars(*hex_colors, animation, self.settings.background_ppi, self.settings.background_alpha, self.settings.background_lightness,
                                                         blur=self.settings.blur_background, blur_radius=self.settings.blur_background_radius)

        return surface.convert()


