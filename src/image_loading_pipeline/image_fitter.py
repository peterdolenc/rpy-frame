import random
import pygame
from entities.image_fitment import ImageFitment
from image_loading_pipeline.helpers.image_resizer import ImageResizer
from thread_context import ThreadContext
from settings import Settings


class ImageFitter:

    def __init__(self, thread_context: ThreadContext):
        self.settings: Settings = thread_context.settings
        self.screen_dimensions = thread_context.gui.get_screen_resolution()

    # Determine how we are fitting the image - by width or by height (or full image)
    def fit_new_image(self, image: pygame.Surface) -> ImageFitment:
        image_ratio = image.get_width() / image.get_height()
        screen_width = self.screen_dimensions[0]
        screen_height = self.screen_dimensions[1]
        screen_ratio = screen_width / screen_height
        use_inner_border = True
        full_screen = False

        resize_width = self.screen_dimensions[0]
        resize_height = self.screen_dimensions[1]

        # portrait (or just square/narrow) image => Screen is wider than the image
        if screen_ratio > image_ratio:
            # natural fitment would be to fit by height and have some black bars on the side
            resize_width = resize_height * image_ratio

        # Panoramic, ultra wide image => Screen is narrower than the image
        else:
            # natural fitment would be to fit it by width and have some black bars on top - bottom
            resize_height = resize_width / image_ratio

        image_fitment = ImageFitment(self.screen_dimensions)
        image_fitment.full_screen = full_screen
        image_fitment.current_image = ImageResizer.resize(image, (resize_width, resize_height), self.settings.border_inner if use_inner_border else 0,
                                                         self.settings.inner_border_color)

        if self.screen_dimensions[0] > image_fitment.current_image.get_width():
            free_space = self.screen_dimensions[0] - image_fitment.current_image.get_width()
            image_fitment.alignment = random.randint(0, free_space)
            if image_fitment.alignment < self.settings.border_outer:
                image_fitment.alignment = 0
            elif free_space - image_fitment.alignment < self.settings.border_outer:
                image_fitment.alignment = free_space

        return image_fitment