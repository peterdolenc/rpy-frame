import pygame

class ImageResizer:
    # resizes the image to target dimensions
    def resize(image: pygame.Surface, dimensions, border: int, border_color) -> pygame.Surface:
        dimensions = (int(dimensions[0]), int(dimensions[1]))
        image_surface = pygame.transform.smoothscale(image, (dimensions[0] - 2 * border, dimensions[1] - 2 * border))
        surface = pygame.Surface(dimensions)
        surface.fill(border_color)
        surface.blit(image_surface, (border, border))
        return surface
