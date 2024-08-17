from queue import Queue
from image_renderer import ImageRenderer
from thread_context import ThreadContext
from settings import Settings


class SlideshowPresenter:
    def __init__(self, presentable_images_queue: Queue, thread_context: ThreadContext):
        self.settings: Settings = thread_context.settings
        self.presentable_images_queue: Queue = presentable_images_queue
        self.image_renderer = ImageRenderer(thread_context)
        self.current_image, self.previous_image = None, None

    # presents next
    def present(self):
        self.previous_image = self.current_image
        self.current_image = self.presentable_images_queue.get()
        self.present_current_image()

    # handles next button pressed by redrawing with info
    def handle_next(self):
        upper_text = "Loading..."
        main_text = "Next button pressed. Preparing your next image..."
        self.image_renderer.draw(self.current_image.fitment, upper_text, main_text)

    # handles previous button press by redrawing previous image
    def handle_back(self):
        self.current_image = self.previous_image
        self.present_current_image()

    # presents a single image
    def present_current_image(self):
        image_meta, fitment = self.current_image.meta, self.current_image.fitment
        date_text = image_meta.date.strftime("%d %B %Y %H:%M")
        caption_text = image_meta.caption
        upper_text = date_text if self.settings.display_date else None
        date_text if self.settings.display_date else None
        main_text = caption_text if self.settings.display_caption else None

        print("Displaying: " + image_meta.full_path + " on screen.")
        self.image_renderer.draw(fitment, upper_text, main_text)

