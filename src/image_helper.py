import pygame


class ImageHelper:

    def resize(image,  dimensions):
        dimensions = (int(dimensions[0]), int(dimensions[1]))
        return pygame.transform.smoothscale(image, dimensions)