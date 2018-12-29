import pygame

from file_loader import FileLoader
from settings import Settings


class Gui:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.mode = max(pygame.display.list_modes())
        # for testing on macbook
        if settings.dev_mode:
            self.mode = (1440, 900)
        pygame.display.set_caption('rpy slideshow')
        pygame.display.set_mode(self.mode, pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.get_surface()
        self.display_loading_logo()


    def get_screen_resolution(self):
        return self.mode

    def display_image(self, image: pygame.Surface, posx: int, posy: int, background: pygame.Surface=None, upper_right_text=None):
        if background is not None:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        if self.settings.border_outer > 0:
            border = self.settings.border_outer
            pygame.draw.rect(self.screen, self.settings.outer_border_color, [posx - border, posy - border, image.get_width() + 2*border, image.get_height() + 2*border])

        self.screen.blit(image, (posx, posy))

        if upper_right_text is not None:
            space = 10
            overlap = 1
            font = pygame.font.SysFont(None, 36)
            text_bg = font.render(upper_right_text, True, (0, 0, 0))
            text = font.render(upper_right_text, True, (255, 255, 255))
            self.screen.blit(text_bg, (self.mode[0] - text.get_width() - space - overlap, space))
            self.screen.blit(text_bg, (self.mode[0] - text.get_width() - space + overlap, space))
            self.screen.blit(text_bg, (self.mode[0] - text.get_width() - space, space - overlap))
            self.screen.blit(text_bg, (self.mode[0] - text.get_width() - space, space + overlap))
            self.screen.blit(text, (self.mode[0] - text.get_width() - space, space))

        pygame.display.update()
        pygame.event.pump()

    def display_loading_logo(self, logo_path='../logo.jpg'):
        file_loader = FileLoader()
        logo = file_loader.load_image(logo_path)
        logo = pygame.transform.scale(logo, self.mode)
        self.screen.blit(logo, (0, 0))
        pygame.display.update()
        pygame.event.pump()



