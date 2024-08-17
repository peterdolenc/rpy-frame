#!/usr/bin/python3
from queue import Queue
import pygame
from gui import Gui
from image_loading_pipeline.image_loader import ImageLoader
from interaction.button_hub import ButtonHub
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
    buttonsHub = ButtonHub(settings)
    
    presenter = create_slideshow_presenter(thread_context)

    # main loopp
    while True:
        start_time = pygame.time.get_ticks()
        end_time = start_time + settings.duration * 1000
        presenter.present()
        while pygame.time.get_ticks() < end_time:
            check_events(buttonsHub)
            if buttonsHub.next_flag_set():
                presenter.handle_next()
                break
            if buttonsHub.back_flag_set():
                presenter.handle_back()


def check_events(buttonsHub: ButtonHub):
    for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        buttonsHub.handle_keydown(event.key)
    

def create_slideshow_presenter(thread_context: ThreadContext):
    presentable_images_queue = Queue(maxsize=thread_context.settings.prepared_images_buffer_size)
    image_loader = ImageLoader(thread_context, presentable_images_queue)
    image_loader.start()
    return SlideshowPresenter(presentable_images_queue, thread_context)

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
