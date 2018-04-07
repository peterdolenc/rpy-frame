import pygame

from entities.image_library import ImageLibrary
from entities.image_meta import ImageMeta
from file_loader import FileLoader
from gui import Gui
from image_renderer import ImageRenderer
from settings import Settings


class SlideshowPresenter:

    def __init__(self, gui: Gui, settings: Settings, image_library: ImageLibrary):
        self.gui: Gui = gui
        self.settings: Settings = settings
        self.image_library: ImageLibrary = image_library
        self.file_loader = FileLoader()
        self.image_renderer = ImageRenderer(settings, gui)

    # presents (indefinitelly)
    def present(self):
        while True:
            sequence = self.image_library.get_sequence()
            print(f'Starting a new sequence with length of {len(sequence):d}')
            for image_meta in sequence:
                self.present_image(image_meta)

    # presents a single image
    def present_image(self, image_meta: ImageMeta):
        image = self.file_loader.load_image(image_meta.full_path)
        self.image_renderer.render_new_image(image)
        start_time = pygame.time.get_ticks()
        duration_millis = self.settings.duration * 1000

        while pygame.time.get_ticks() < start_time + duration_millis:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress_state = min(elapsed_time / duration_millis, 1.0)
            self.image_renderer.draw(progress_state)
            elapsed_time_after = pygame.time.get_ticks() - start_time
            self.check_for_quit()
            additional_delay = max(0, (50 - (elapsed_time_after - elapsed_time)))
            pygame.time.wait(additional_delay)

    # checks if quit buttons were pressed
    def check_for_quit(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE] or keys[pygame.K_q] or keys[pygame.K_x] or keys[
            pygame.K_z]:
            exit(0)

