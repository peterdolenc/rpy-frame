import os
import time
import pygame

from io_thread.keyboard_debouncer import KeyboardDebouncer
from io_thread.thread_context import ThreadContext


class IoMain():
    def __init__(self, thread_context: ThreadContext, pygame: pygame):
        self.thread_context = thread_context
        self.pygame = pygame
        self.settings = thread_context.settings

    def start(self):
        if IoMain.is_rbpi():
            import RPi.GPIO as GPIO
            from io_thread.phisical_button_handler import PhisicalButtonHandler
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.settings.physical_button_pin, GPIO.IN)
            cb = PhisicalButtonHandler(self.settings.physical_button_pin, self.button_handler, bouncetime=100)
            cb.start()
            GPIO.add_event_detect(self.settings.physical_button_pin, GPIO.RISING, callback=cb)

        left_key = KeyboardDebouncer(pygame, [pygame.K_RIGHT, pygame.HAT_RIGHT], (lambda _: self.button_handler(self.settings.physical_button_longpress_duration+1)))
        left_key.start()

        space_key = KeyboardDebouncer(pygame, [pygame.K_SPACE, pygame.K_RETURN], self.button_handler)
        space_key.start()

        quit_key = KeyboardDebouncer(pygame, [pygame.K_ESCAPE, pygame.K_q], self.trigger_quit)
        quit_key.start()

        while True:
            left_key.__call__()
            space_key.__call__()
            quit_key.__call__()
            time.sleep(0.1)


    @staticmethod
    def is_rbpi():
        return os.uname()[4][:3] == 'arm'

    def button_handler(self, duration):
        print("Physical button pressed with duration: " + str(duration) + " ms")

        if duration > self.settings.physical_button_longpress_duration:
            self.trigger_long_press()
        else:
            self.trigger_short_press()

    def trigger_long_press(self):
        for handler in self.thread_context.button_long_press_handlers:
            handler()

    def trigger_short_press(self):
        for handler in self.thread_context.button_short_press_handlers:
            handler()

    def trigger_quit(self, _):
        print("Quit button pressed.")
        for handler in self.thread_context.button_quit_handlers:
            handler()



