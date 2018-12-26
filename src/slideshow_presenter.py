import pygame

from background_helper import BackgroundHelper
from entities.image_library import ImageLibrary
from entities.image_meta import ImageMeta
from file_loader import FileLoader
from gui import Gui
from image_helper import ImageHelper
from image_renderer import ImageRenderer
from io_thread.thread_context import ThreadContext
from settings import Settings


class SlideshowPresenter:

    def __init__(self, gui: Gui, settings: Settings, image_library: ImageLibrary, thread_context: ThreadContext):
        self.gui: Gui = gui
        self.settings: Settings = settings
        self.image_library: ImageLibrary = image_library
        self.file_loader = FileLoader()
        self.image_renderer = ImageRenderer(settings, gui)
        self.background_helper = BackgroundHelper(gui.get_screen_resolution(), settings)
        self.thread_context = thread_context
        self.go_next = False

        self.thread_context.button_long_press_handlers.append(self.next_image_handler)

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
        date_text = image_meta.date.strftime("%d %B %Y %H:%M")

        while pygame.time.get_ticks() < start_time + duration_millis:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress_state = min(elapsed_time / duration_millis, 1.0)
            upper_text = date_text if self.settings.display_date else None
            if self.go_next:
                upper_text = "Loading next..."
            self.image_renderer.draw(progress_state, fitment, upper_text)
            elapsed_time_after = pygame.time.get_ticks() - start_time
            if self.go_next:
                self.go_next = False
                break
            additional_delay = max(0, (50 - (elapsed_time_after - elapsed_time)))
            pygame.time.wait(additional_delay)

    # longpress handler that moves image next
    def next_image_handler(self):
        print("Advancing to the next image...")
        self.go_next = True