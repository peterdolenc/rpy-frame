import pygame

from file_loader import FileLoader
from gui import Gui
from image_helper import ImageHelper


def main():
    image_helper = ImageHelper()
    gui = Gui()
    file_loader = FileLoader()

    files = file_loader.get_files()
    print(files)





    for file in files:
        image = file_loader.load_image(file)
        resized = image_helper.resize(image, gui.get_screen_resolution())
        for i in range(-50, 50):
            gui.display_image(resized, i, i)
            pygame.time.delay(50)





if __name__ == "__main__":
    main()
