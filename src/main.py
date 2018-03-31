import pygame

from file_loader import FileLoader
from gui import Gui


def main():
    file_loader = FileLoader()

    files = file_loader.get_files()
    print(files)



    gui = Gui()


    for file in files:
        image = file_loader.load_image(file)
        gui.display_image(image)
        pygame.time.delay(5000)





if __name__ == "__main__":
    main()
