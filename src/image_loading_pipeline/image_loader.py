import threading
from queue import Queue

from entities.presentable_image import PresentableImage
from image_loading_pipeline.background_maker import BackgroundMaker
from image_loading_pipeline.helpers.dominant_color_extractor import (
    DominantColorExtractor,
)
from image_loading_pipeline.helpers.file_loader import FileLoader
from image_loading_pipeline.image_fitter import ImageFitter
from image_loading_pipeline.image_library import ImageLibrary
from thread_context import ThreadContext
from settings import Settings


class ImageLoader(threading.Thread):
    def __init__(self, thread_context: ThreadContext, presentable_images_queue: Queue):
        super(ImageLoader, self).__init__()
        self.settings: Settings = thread_context.settings
        self.gui = thread_context.gui
        self.image_fitter = ImageFitter(thread_context)
        self.image_library = ImageLibrary(thread_context)
        self.image_library.initialize()
        self.background_maker = BackgroundMaker(
            self.gui.get_screen_resolution(), self.settings
        )
        self.presentable_images_queue = presentable_images_queue
        self.stop_request = threading.Event()

        self.current_sequence = None
        self.current_index = -1

    # initializes the image library by detecting metadata and sorting images
    def run(self):
        self.current_sequence = self.image_library.get_sequence()

        while not self.stop_request.isSet():
            try:
                meta = self.next_image_meta()
                try:
                    print("[bg image loader]: preparing: " + meta.full_path)
                    img = self.load_and_fit_image(meta)
                    self.presentable_images_queue.put(img)
                except Exception as e:
                    print("[bg image loader]: error loading: " + meta.full_path)
                    print(e)
            except Exception as e:
                print(e)

    def next_image_meta(self):
        self.current_index += 1
        if self.current_index >= len(self.current_sequence):
            self.current_sequence = self.image_library.get_sequence()
            self.current_index = 0
        return self.current_sequence[self.current_index]

    def load_and_fit_image(self, image_meta):
        image = FileLoader.load_image(image_meta.full_path)
        fitment = self.image_fitter.fit_new_image(image)
        if not fitment.full_screen:
            dominant_colors = DominantColorExtractor.get_dominant_colors(
                image_meta, fitment.current_image
            )
            if self.settings.background_patterns:
                fitment.current_background = self.background_maker.get_dominant_pattern(dominant_colors)
            else:
                fitment.current_background = self.background_maker.get_dominant_color_fill(dominant_colors)
        return PresentableImage(image_meta, fitment)
