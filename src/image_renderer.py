from entities.image_fitment import ImageFitment
from gui import Gui
import time

class ImageRenderer:
    def __init__(self, gui: Gui):
        self.gui: Gui = gui
        self.screen_dimensions = self.gui.get_screen_resolution()

    def draw(self, fitment: ImageFitment, upper_text=None, main_text=None):
        center_x = (self.screen_dimensions[0] - fitment.current_image.get_width()) / 2
        center_y = (self.screen_dimensions[1] - fitment.current_image.get_height()) / 2

        if self.screen_dimensions[0] > fitment.current_image.get_width():
            center_x = fitment.alignment

        # todo: split render and display
        self.gui.display_image(
            fitment.current_image,
            center_x,
            center_y,
            fitment.current_background,
            upper_text,
            main_text,
        )
        
        time.sleep(0.001)

        self.gui.display_image(
            fitment.current_image,
            center_x,
            center_y,
            fitment.current_background,
            upper_text,
            main_text,
        )
