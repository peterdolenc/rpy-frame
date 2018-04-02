import pygame


class ImageHelper:

    def resize(self, image,  dimensions):
        return pygame.transform.smoothscale(image, dimensions)