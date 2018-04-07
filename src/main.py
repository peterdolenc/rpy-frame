from entities.image_library import ImageLibrary
from file_loader import FileLoader
from gui import Gui
from settings import Settings
from slideshow_presenter import SlideshowPresenter


def main():
    gui = Gui()
    settings = Settings()
    file_loader = FileLoader()
    image_paths = file_loader.discover_images()
    image_library = ImageLibrary()
    image_library.initialize(image_paths)
    slideshow_presenter = SlideshowPresenter(gui, settings, image_library)
    slideshow_presenter.present()


if __name__ == "__main__":
    main()


# TODO:
# Background must not be black but of dominant color
# More configurability
# Channel to print data on screen
