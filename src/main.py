#!/usr/bin/env python3.6
import _thread
import os

import pygame

from entities.image_library import ImageLibrary
from file_loader import FileLoader
from gui import Gui
from io_thread.io_main import IoMain
from settings import Settings
from slideshow_presenter import SlideshowPresenter
import sys

from io_thread.thread_context import ThreadContext


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
    pygame.init()
    settings = Settings()
    thread_context = ThreadContext(settings)
    thread_context.button_quit_handlers.append(lambda: os._exit(0))
    _thread.start_new_thread(start_io_thread, (thread_context, pygame))

    # main thread
    start_presentation_thread(thread_context)


def start_presentation_thread(thread_context):
    parse_cmd_args(thread_context.settings)
    gui = Gui(thread_context.settings)
    file_loader = FileLoader()
    image_paths = file_loader.discover_images(thread_context.settings.media_folder)
    image_library = ImageLibrary()
    image_library.initialize(image_paths)
    slideshow_presenter = SlideshowPresenter(gui, thread_context.settings, image_library, thread_context)
    slideshow_presenter.present()


def start_io_thread(thread_context: ThreadContext, pygame: pygame):
    def short_press_handler():
        thread_context.settings.display_date = not thread_context.settings.display_date
    thread_context.button_short_press_handlers.append(short_press_handler)
    io_main = IoMain(thread_context, pygame)
    io_main.start()



if __name__ == "__main__":
    main()


# TODO:
# print image comment on screen
# Enable more backgrounds
# Optimize dominant color calc and background creation when image is displayed fullscreen
# Add movie support

# TODO / MAYBE
# Animated backgrounds?
# Image transitions?
# Image effects (2 images merged?)
# Optimizations?
