from entities.image_fitment import Fitment, ImageFitment
from gui import Gui
from thread_context import ThreadContext
from settings import Settings


class ImageRenderer:
    def __init__(self, thread_context: ThreadContext):
        self.gui: Gui = thread_context.gui
        self.screen_dimensions = self.gui.get_screen_resolution()

        self.settings: Settings = thread_context.settings

    # Draw the image at the correct position regarding to how much time is left
    def draw(
        self, progress: float, fitment: ImageFitment, upper_text=None, main_text=None
    ):

        # TODO just get rid of prorgess
        # elapsed = 1.0 - progress
        center_x = (self.screen_dimensions[0] - fitment.current_image.get_width()) / 2
        center_y = (self.screen_dimensions[1] - fitment.current_image.get_height()) / 2

        if self.screen_dimensions[0] > fitment.current_image.get_width():
            center_x = fitment.alignment

        # if fitment.current_fitment == Fitment.HORIZONTAL_SCROLL:
        # center_x = int((-1) * fitment.end_position * elapsed)
        # elif fitment.current_fitment == Fitment.VERTICAL_SCROLL:
        # center_y = int(-1 * fitment.end_position * elapsed)

        print(f"center_x {center_x}  center_y {center_y}")

        self.gui.display_image(
            fitment.current_image,
            center_x,
            center_y,
            fitment.current_background,
            upper_text,
            main_text,
        )
