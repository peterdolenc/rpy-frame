from gui import Gui
from settings import Settings


class ThreadContext:
    def __init__(self, settings: Settings, gui: Gui):
        # context objects
        self.settings = settings
        self.gui = gui

        # event handlers
        self.button_short_press_handlers = []
        self.button_long_press_handlers = []
        self.button_quit_handlers = []
