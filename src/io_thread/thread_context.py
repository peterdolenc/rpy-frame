class ThreadContext:
    def __init__(self, settings):
        self.button_short_press_handlers = []
        self.button_long_press_handlers = []
        self.button_quit_handlers = []
        self.settings = settings
