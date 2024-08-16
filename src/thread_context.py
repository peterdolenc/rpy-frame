from gui import Gui
from settings import Settings

# TODO: remove
class ThreadContext:
    def __init__(self, settings: Settings, gui: Gui):
        # context objects
        self.settings = settings
        self.gui = gui

