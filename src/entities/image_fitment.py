import pygame
from enum import Enum


class Fitment(Enum):
    VERTICAL_SCROLL = 0,
    HORIZONTAL_SCROLL = 1,
    STILL = 3


class ImageFitment:

    def __init__(self, screen_dimensions):
        self.screen_dimensions = screen_dimensions
        self.current_fitment = Fitment.STILL
        self.end_position = 0
        self.current_image = None
        self.current_background = None
