from entities.image_library import ImageLibrary
from file_loader import FileLoader
from gui import Gui
from settings import Settings
from slideshow_presenter import SlideshowPresenter
import sys


def get_image_path(settings: Settings):
    if len(sys.argv) > 1:
        settings.media_folder = sys.argv[1]
    print(f"Using {settings.media_folder} as media directory.")

def main():
    gui = Gui()
    settings = Settings()
    get_image_path(settings)
    file_loader = FileLoader()
    image_paths = file_loader.discover_images(settings.media_folder)
    image_library = ImageLibrary()
    image_library.initialize(image_paths)
    slideshow_presenter = SlideshowPresenter(gui, settings, image_library)
    slideshow_presenter.present()


if __name__ == "__main__":
    main()


# TODO:
# More configurability
# Channel to print data on screen
# Align images randomly
