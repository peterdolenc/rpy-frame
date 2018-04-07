import pygame

from file_loader import FileLoader
from gui import Gui
from image_renderer import ImageRenderer
from settings import Settings


def check_for_quit():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE] or keys[pygame.K_q] or keys[pygame.K_x] or keys[pygame.K_z]:
        exit(0)


def main():
    gui = Gui()
    file_loader = FileLoader()
    settings = Settings()
    image_renderer = ImageRenderer(settings, gui)

    files = file_loader.get_files()
    print(files)


    for file in files:
        image = file_loader.load_image(file)
        image_renderer.render_new_image(image)
        start_time = pygame.time.get_ticks()
        duration_millis = settings.duration * 1000

        while pygame.time.get_ticks() < start_time + duration_millis:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress_state = min(elapsed_time / duration_millis, 1.0)
            image_renderer.draw(progress_state)
            elapsed_time_after = pygame.time.get_ticks() - start_time
            check_for_quit()
            additional_delay = max(0, (50 - (elapsed_time_after - elapsed_time)))
            pygame.time.wait(additional_delay)


if __name__ == "__main__":
    main()


# TODO:
# It needs to collect metadata
# It needs to provide images in chunks of files that were created closer together
# Background must not be black but of dominant color
