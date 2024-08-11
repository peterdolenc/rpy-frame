import pygame

class ImageFitment:

    def __init__(self, screen_dimensions):
        self.screen_dimensions = screen_dimensions
        self.current_image: pygame.Surface = None
        self.current_background: pygame.Surface = None
        self.alignment = 0
        self.full_screen = False
