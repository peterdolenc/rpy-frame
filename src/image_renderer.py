from entities.image_fitment import ImageFitment
from gui import Gui
from thread_context import ThreadContext
from settings import Settings


class ImageRenderer:
    def __init__(self, thread_context: ThreadContext):
        self.gui: Gui = thread_context.gui
        self.screen_dimensions = self.gui.get_screen_resolution()
        self.settings: Settings = thread_context.settings

    def draw(
        self, fitment: ImageFitment, upper_text=None, main_text=None
    ):
        center_x = (self.screen_dimensions[0] - fitment.current_image.get_width()) / 2
        center_y = (self.screen_dimensions[1] - fitment.current_image.get_height()) / 2

        if self.screen_dimensions[0] > fitment.current_image.get_width():
            center_x = fitment.alignment

        self.gui.display_image(
            fitment.current_image,
            center_x,
            center_y,
            fitment.current_background,
            upper_text,
            main_text,
        )
