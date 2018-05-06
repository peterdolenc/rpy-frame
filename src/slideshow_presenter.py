import pygame

from background_helper import BackgroundHelper
from entities.image_library import ImageLibrary
from entities.image_meta import ImageMeta
from file_loader import FileLoader
from gui import Gui
from image_helper import ImageHelper
from image_renderer import ImageRenderer
from settings import Settings


class SlideshowPresenter:

    def __init__(self, gui: Gui, settings: Settings, image_library: ImageLibrary):
        self.gui: Gui = gui
        self.settings: Settings = settings
        self.image_library: ImageLibrary = image_library
        self.file_loader = FileLoader()
        self.image_renderer = ImageRenderer(settings, gui)
        self.background_helper = BackgroundHelper(gui.get_screen_resolution(), settings)

    # presents (indefinitely)
    def present(self):
        while True:
            sequence = self.image_library.get_sequence()
            print(f'Starting a new sequence with length of {len(sequence):d}')
            for image_meta in sequence:
                self.present_image(image_meta)

    # presents a single image
    def present_image(self, image_meta: ImageMeta):
        image = self.file_loader.load_image(image_meta.full_path)
        fitment = self.image_renderer.fit_new_image(image)
        dominant_colors = ImageHelper.get_dominant_colors(image_meta, fitment.current_image)
        fitment.current_background = self.background_helper.get_dominant_pattern(dominant_colors)
        start_time = pygame.time.get_ticks()
        duration_millis = self.settings.duration * 1000
        upper_text = image_meta.date.strftime("%d %B %Y %H:%M") if self.settings.display_date else None

        while pygame.time.get_ticks() < start_time + duration_millis:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress_state = min(elapsed_time / duration_millis, 1.0)
            # fitment.current_background = self.background_helper.get_dominant_pattern(dominant_colors, progress_state)
            self.image_renderer.draw(progress_state, fitment, upper_text)
            elapsed_time_after = pygame.time.get_ticks() - start_time
            self.check_for_quit()
            if self.check_for_next():
                break
            additional_delay = max(0, (50 - (elapsed_time_after - elapsed_time)))
            pygame.time.wait(additional_delay)

    # checks if quit buttons were pressed
    def check_for_quit(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE] or keys[pygame.K_q] or keys[pygame.K_x] or keys[
            pygame.K_z]:
            exit(0)

    # checks if right arrow key button was presed
    def check_for_next(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_RIGHT] or keys[pygame.HAT_RIGHT]