from queue import Queue
import pygame
from entities.image_meta import ImageMeta
from image_renderer import ImageRenderer
from thread_context import ThreadContext
from settings import Settings


class SlideshowPresenter:
    def __init__(self, presentable_images_queue: Queue, thread_context: ThreadContext):
        self.settings: Settings = thread_context.settings
        self.presentable_images_queue: Queue = presentable_images_queue
        self.image_renderer = ImageRenderer(thread_context)
        self.thread_context = thread_context
        self.go_next = False
        self.thread_context.button_long_press_handlers.append(self.next_image_handler)

    # presents (indefinitely)
    def present(self):
        while True:
            presentable_image = self.presentable_images_queue.get()
            self.present_image(presentable_image.meta, presentable_image.fitment)

    # presents a single image
    def present_image(self, image_meta: ImageMeta, fitment):
        start_time = pygame.time.get_ticks()
        duration_millis = self.settings.duration * 1000
        # date_text = image_meta.date.strftime("%d %B %Y %H:%M")
        caption_text = image_meta.caption

        while pygame.time.get_ticks() < start_time + duration_millis:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress_state = min(elapsed_time / duration_millis, 1.0)
            # upper_text = date_text if self.settings.display_date else None
            upper_text = ""
            # date_text if self.settings.display_date else None
            main_text = caption_text if self.settings.display_caption else None
            go_next_detected = self.go_next
            if go_next_detected:
                upper_text = "Loading..."
                main_text = "Next button pressed. Preparing your next image..."
            self.image_renderer.draw(progress_state, fitment, upper_text, main_text)
            elapsed_time_after = pygame.time.get_ticks() - start_time
            if go_next_detected:
                self.go_next = False
                break
            additional_delay = max(0, (50 - (elapsed_time_after - elapsed_time)))
            pygame.time.wait(additional_delay)

    # longpress handler that moves image next
    def next_image_handler(self):
        print("Advancing to the next image...")
        self.go_next = True
