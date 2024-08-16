import os
import sys

import pygame

from image_loading_pipeline.helpers.file_loader import FileLoader
from settings import Settings


class Gui:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.mode = max(pygame.display.list_modes())
        # for testing on macbook
        if settings.dev_mode:
            self.mode = (1920, 1080)
        pygame.display.set_caption("rpy slideshow")
        pygame.display.set_mode(self.mode, pygame.DOUBLEBUF | pygame.HWSURFACE)
        if settings.fullscreen:
            pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.get_surface()
        self.display_loading_logo()

    def get_screen_resolution(self):
        return self.mode

    def display_image(
        self,
        image: pygame.Surface,
        posx: int,
        posy: int,
        background: pygame.Surface = None,
        upper_right_text: str = None,
        main_text: str = None,
    ):
        if background is not None:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        if self.settings.border_outer > 0:
            border = self.settings.border_outer
            pygame.draw.rect(
                self.screen,
                self.settings.outer_border_color,
                [
                    posx - border,
                    posy - border,
                    image.get_width() + 2 * border,
                    image.get_height() + 2 * border,
                ],
            )

        self.screen.blit(image, (posx, posy))

        if upper_right_text is not None:
            self.render_upper_right_text(upper_right_text)

        if main_text is not None:
            line = 0
            words = main_text.split(" ")
            words.reverse()
            text = ""
            for word in words:
                text = word + " " + text
                if len(text) > self.settings.image_comment_target_line_length:
                    self.render_main_text(text, line)
                    line += 1
                    text = ""
            self.render_main_text(text, line)

        pygame.display.update()
        pygame.event.pump()

    def render_upper_right_text(self, text, font=36):
        space = 10
        font = pygame.font.SysFont(None, font)
        text_bg = font.render(text, True, (0, 0, 0))
        text = font.render(text, True, (255, 255, 255))
        x = self.mode[0] - text.get_width() - space
        y = space
        self.render_texts_at_popsition(text, text_bg, x, y)

    def render_main_text(self, text: str, line=0, font_size=30):
        gap = 80
        font = pygame.font.SysFont(None, font_size)
        text_bg = font.render(text, True, (0, 0, 0))
        text_fg = font.render(text, True, (255, 255, 255))
        x = (self.mode[0] - text_fg.get_width()) / 2
        y = (
            self.mode[1]
            - text_fg.get_height()
            - gap
            - line * (text_fg.get_height() + 5)
        )
        self.render_texts_at_popsition(text_fg, text_bg, x, y)

    def render_texts_at_popsition(self, text, text_bg, x, y):
        overlap = 1
        self.screen.blit(text_bg, (x - overlap, y))
        self.screen.blit(text_bg, (x + overlap, y))
        self.screen.blit(text_bg, (x, y - overlap))
        self.screen.blit(text_bg, (x, y + overlap))
        self.screen.blit(text, (x, y))

    def display_loading_logo(self, logo_path="/../logo.jpg"):
        logo = FileLoader.load_image(os.path.realpath(sys.path[0]) + logo_path)
        logo = pygame.transform.scale(logo, self.mode)
        self.screen.blit(logo, (0, 0))
        pygame.display.update()
        pygame.event.pump()
