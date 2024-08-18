#!/usr/bin/python3
from queue import Queue
import pygame
from gui import Gui
from image_loading_pipeline.image_loader import ImageLoader
from interaction.api_server import ApiServer
from interaction.button_hub import ButtonHub
from settings import Settings
from slideshow_presenter import SlideshowPresenter
import sys
from thread_context import ThreadContext
import threading

def parse_cmd_args(settings: Settings):
    if len(sys.argv) > 2:
        settings.media_folder = sys.argv[1]
        settings.media_folder_secondary = sys.argv[2]
    elif len(sys.argv) == 2:
        settings.media_folder = sys.argv[1]
        if sys.argv[1] == 'dev':
            settings.dev_mode = True
            settings.duration = 20
            settings.fullscreen = False
            settings.media_folder = "../samples"
            print("Running in dev mode.")
    print(f"Using {settings.media_folder} as media directory.")
    if settings.media_folder_secondary: 
         print(f"Using {settings.media_folder_secondary} as secondary media directory.")

def main():
    pygame.init()
    settings = Settings()
    parse_cmd_args(settings)
    gui = Gui(settings)
    thread_context = ThreadContext(settings, gui)
    buttonHub = ButtonHub(settings)
    if settings.api_enabled:
        api = ApiServer(settings, buttonHub)
        threading.Thread(target=api.start_bg).start()
    presenter = SlideshowPresenter(thread_context, settings.media_folder, settings.prepared_images_buffer_size)
    primaryPresenter, secondaryPresenter = presenter, presenter
    if settings.media_folder_secondary: 
        secondaryPresenter = SlideshowPresenter(thread_context, settings.media_folder_secondary, 1)

    # main loopp
    while True:
        start_time = pygame.time.get_ticks()
        end_time = start_time + settings.duration * 1000
        presenter.present()
        while pygame.time.get_ticks() < end_time:
            check_events(buttonHub)
            if buttonHub.next_flag_set():
                presenter.handle_next()
                break
            if buttonHub.back_flag_set():
                presenter.handle_back()
            if buttonHub.switch_to_secondary_flag_set():
                presenter = secondaryPresenter
                break
            if buttonHub.switch_to_primary_flag_set():
                presenter = primaryPresenter
                break


def check_events(buttonHub: ButtonHub):
    for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        buttonHub.handle_keydown(event.key)
    

if __name__ == "__main__":
    main()


# TODO:
# Reduce alpha of solid image bg
# Prioritize (weighted) images taken on the same day from previous years
# Find out image average brightness and adjust backgrounds to match it (one stop darker bit darker)
# Double-tap: skip the whole sequence
# Read camera/lens information and display it
# Transition when changing image

# TODO / MAYBE
# Layout where image is on the side and on the other side the date and the caption are displaye
# Enable more backgrounds
# Add movie support
