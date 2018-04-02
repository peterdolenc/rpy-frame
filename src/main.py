import pygame

from file_loader import FileLoader
from gui import Gui
from image_renderer import ImageRenderer
from settings import Settings


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
            additional_delay = max(0, (50 - (elapsed_time_after - elapsed_time)))
            print('delay of ' + str(additional_delay) + ' added')
            pygame.time.wait(additional_delay)



if __name__ == "__main__":
    main()



# TODO:
# 2. Fullscreen + handling of Q/Esc