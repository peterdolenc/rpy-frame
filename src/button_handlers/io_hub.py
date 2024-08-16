import os
import time
import pygame

from settings import Settings

class IoHub():
    def __init__(self, settings: Settings):
        self.settings = settings
        self.button_short_press_handlers = []
        self.button_long_press_handlers = []
        self.button_quit_handlers = []
        self.pending_next = False

        self.button_long_press_handlers.append(self.next_button_handler)
        self.button_short_press_handlers.append(self.short_press_handler)
        self.button_quit_handlers.append(lambda: os._exit(0))

        if IoHub.is_rbpi():
            import RPi.GPIO as GPIO
            from io_hub.phisical_button_handler import PhisicalButtonHandler
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.settings.physical_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            cb = PhisicalButtonHandler(self.settings.physical_button_pin, self.button_handler, bouncetime=150)
            cb.start()
            GPIO.add_event_detect(self.settings.physical_button_pin, GPIO.BOTH, callback=cb)

    @staticmethod
    def is_rbpi():
        return os.uname()[4][:3] == 'arm'

    def handle_keydown(self, key_code):
        if key_code == pygame.K_SPACE or key_code == pygame.K_RETURN: 
            self.trigger_short_press()
        elif key_code == pygame.K_RIGHT or key_code == pygame.HAT_RIGHT: 
            self.trigger_long_press()
        elif key_code == pygame.K_ESCAPE or key_code == pygame.K_q:
            self.trigger_quit()

    def button_handler(self, duration):
        print("Physical button pressed with duration: " + str(duration) + " ms")

        if duration > self.settings.physical_button_longpress_duration:
            self.trigger_long_press()
        else:
            self.trigger_short_press()

    def trigger_long_press(self):
        print("Long press.")
        for handler in self.button_long_press_handlers:
            handler()

    def trigger_short_press(self):
        print("Short press.")
        for handler in self.button_short_press_handlers:
            handler()

    def trigger_quit(self):
        print("Quit button pressed.")
        for handler in self.button_quit_handlers:
            handler()

    def next_flag_set(self):
        if self.pending_next:
            self.pending_next = False
            return True
        return False

    def short_press_handler(self):
        self.settings.display_date = not self.settings.display_date
        self.settings.display_caption = self.settings.display_date

    def next_button_handler(self):
        self.pending_next = True


        
    