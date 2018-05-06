import pygame
from settings import Settings


class Gui:

    def __init__(self, settings: Settings):
        self.settings = settings
        pygame.init()
        self.mode = max(pygame.display.list_modes())
        # for testing on macbook
        if settings.dev_mode:
            self.mode = (1440, 900)
        pygame.display.set_caption('rpy slideshow')
        pygame.display.set_mode(self.mode, pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.get_surface()
        self.screen.fill((0, 0, 0))

    def get_screen_resolution(self):
        return self.mode

    def display_image(self, image: pygame.Surface, posx: int, posy: int, background: pygame.Surface=None):
        self.screen.fill((0, 0, 0))
        if background is not None:
            self.screen.blit(background, (0, 0))

        if self.settings.border_outer > 0:
            border = self.settings.border_outer
            pygame.draw.rect(self.screen, self.settings.outer_border_color, [posx - border, posy - border, image.get_width() + 2*border, image.get_height() + 2*border])

        self.screen.blit(image, (posx, posy))
        pygame.display.update()
        pygame.event.pump()



