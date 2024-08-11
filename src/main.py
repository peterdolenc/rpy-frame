#!/usr/bin/env python3.6
import _thread
import os
from queue import Queue
import pygame
from gui import Gui
from image_loading_pipeline.image_loader import ImageLoader
from io_thread.io_main import IoMain
from settings import Settings
from slideshow_presenter import SlideshowPresenter
import sys

from thread_context import ThreadContext


def parse_cmd_args(settings: Settings):
    if len(sys.argv) > 1:
        if sys.argv[1] == 'dev':
            settings.dev_mode = True
            settings.duration = 20
            settings.fullscreen = False
            print("Running in dev mode.")
        else:
            settings.media_folder = sys.argv[1]
    print(f"Using {settings.media_folder} as media directory.")


def main():
    pygame.init()
    settings = Settings()
    parse_cmd_args(settings)
    gui = Gui(settings)
    thread_context = ThreadContext(settings, gui)
    thread_context.button_quit_handlers.append(lambda: os._exit(0))
    _thread.start_new_thread(start_io_thread, (thread_context, pygame))

    # main thread
    start_presentation_thread(thread_context)


def start_presentation_thread(thread_context: ThreadContext):
    presentable_images_queue = Queue(maxsize=thread_context.settings.prepared_images_buffer_size)
    image_loader = ImageLoader(thread_context, presentable_images_queue)
    image_loader.start()
    slideshow_presenter = SlideshowPresenter(presentable_images_queue, thread_context)
    slideshow_presenter.present()


def start_io_thread(thread_context: ThreadContext, pygame: pygame):
    def short_press_handler():
        thread_context.settings.display_date = not thread_context.settings.display_date
        thread_context.settings.display_caption = thread_context.settings.display_date
    thread_context.button_short_press_handlers.append(short_press_handler)
    io_main = IoMain(thread_context, pygame)
    io_main.start()



if __name__ == "__main__":
    main()


# TODO:
# Super-long-press: skip the whole sequence
# Read camera/lens information and display it
# Transition when changing image


# TODO / MAYBE
# Layout where image is on the side and on the other side the date and the caption are displaye
# Backgrounds where a pattern is made of the current image
# Enable more backgrounds
# Add movie support
# Animated backgrounds?
# Image transitions?
# Image effects (2 images merged?)
