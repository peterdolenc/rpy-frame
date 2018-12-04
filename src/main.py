#!/usr/bin/env python3.6
import _thread
import time

from entities.image_library import ImageLibrary
from file_loader import FileLoader
from gui import Gui
from settings import Settings
from slideshow_presenter import SlideshowPresenter
import os
import sys

from thread_context import ThreadContext


def parse_cmd_args(settings: Settings):
    if len(sys.argv) > 1:
        if sys.argv[1] == 'dev':
            settings.dev_mode = True
            settings.duration = 20
            print("Running in dev mode.")
        else:
            settings.media_folder = sys.argv[1]
    print(f"Using {settings.media_folder} as media directory.")


def main():
    thread_context = ThreadContext()

    _thread.start_new_thread(start_io_thread, (thread_context,))

    # main thread
    start_presentation_thread(thread_context)


def start_presentation_thread(thread_context):
    settings = Settings()
    parse_cmd_args(settings)
    gui = Gui(settings)
    file_loader = FileLoader()
    image_paths = file_loader.discover_images(settings.media_folder)
    image_library = ImageLibrary()
    image_library.initialize(image_paths)
    slideshow_presenter = SlideshowPresenter(gui, settings, image_library, thread_context)
    slideshow_presenter.present()


def start_io_thread(thread_context):

    if is_rbpi():
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(23, GPIO.IN)

    while True:

        if is_rbpi():
            input = GPIO.input(23)
            if input == 1:
                print("Phisical button on pin 23 pressed.")
                thread_context.button_pressed = True
                time.sleep(60)

        time.sleep(1)


def is_rbpi():
    return os.uname()[4][:3] == 'arm'


if __name__ == "__main__":
    main()


# TODO:
# Enable more backgrounds
# Channel to print data on screen
# - print date on screen (configurable)
# - print image comment on screen
# Hardware button listener (use pin 11)
# - listen for single press and long press
# Hardware button action: display date
# Hardware button action: next image (works only once)
# Optimize dominant color calc and background creation when image is displayed fullscreen
# Add movie support

# TODO / MAYBE
# Animated backgrounds?
# Image transitions?
# Image effects (2 images merged?)
# Optimizations?
