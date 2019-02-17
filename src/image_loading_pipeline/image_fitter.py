import random
import pygame
from entities.image_fitment import ImageFitment, Fitment
from image_loading_pipeline.helpers.image_resizer import ImageResizer
from thread_context import ThreadContext
from settings import Settings


class ImageFitter:

    def __init__(self, thread_context: ThreadContext):
        self.settings: Settings = thread_context.settings
        self.screen_dimensions = thread_context.gui.get_screen_resolution()

    # Determine how we are fitting the image - by width or by height (or full image)
    # Determine how much you have to zoom in in order to keep the black area in the range of the setting
    # Determine - if we animate by a single pixel - how many steps do we have in animation
    def fit_new_image(self, image: pygame.Surface) -> ImageFitment:
        image_ratio = image.get_width() / image.get_height()
        screen_width = self.screen_dimensions[0]
        screen_height = self.screen_dimensions[1]
        screen_ratio = screen_width / screen_height
        end_position = 0
        use_inner_border = True
        full_screen = False

        resize_width = self.screen_dimensions[0]
        resize_height = self.screen_dimensions[1]

        # portrait (or just square/narrow) image => Screen is wider than the image
        if screen_ratio > image_ratio:

            # natural fitment would be to fit by height and have some black bars on the side
            current_fitment = Fitment.STILL
            resize_width = resize_height * image_ratio

            # calculate gap/border area to assess better fitment
            gap_area = (screen_width - resize_width) / screen_width

            # if minimum gap area should be eliminated then we fit image by width
            # and let the height of the image be higher than the screen height
            is_less_than_min_gap_area = self.settings.portrait_edge_min > 0 and self.settings.portrait_edge_min > gap_area

            # or if the black area exceeds max amount of black area allowed we also zoom in
            # and let the image be scrolled vertically
            is_more_than_max_gap_area = self.settings.portrait_edge_max < 1 and self.settings.portrait_edge_max < gap_area

            # in either case we do vertical scrolling
            if is_less_than_min_gap_area or is_more_than_max_gap_area:
                current_fitment = Fitment.VERTICAL_SCROLL

                # less than min gap area fitment is fitted by width
                if is_less_than_min_gap_area:
                    resize_width = screen_width
                    use_inner_border = False
                    full_screen = True
                elif is_more_than_max_gap_area:
                    resize_width = screen_width * (1.0 - self.settings.portrait_edge_max)

                resize_height = resize_width / image_ratio
                end_position = resize_height - screen_height

        # Panoramic, ultra wide image => Screen is narrower than the image
        else:

            # natural fitment would be to fit it by width and have some black bars on top - bottom
            current_fitment = Fitment.STILL
            resize_height = resize_width / image_ratio

            # calculate gap/border area to assess better fitment
            gap_area = (screen_height - resize_height) / screen_height

            # if minimum gap area should be eliminated then we fit this image by height
            # and let the width of the image be wider than the screen width
            is_less_than_min_gap_area = self.settings.wide_edge_min > 0 and self.settings.wide_edge_min > gap_area

            # or if the black area exceeds max amount of black area allowed we also zoom in
            # and let the image be scrolled horizontally
            is_more_than_max_gap_area = self.settings.wide_edge_max < 1 and self.settings.wide_edge_max < gap_area

            # in either case we do horizontal scrolling
            if is_more_than_max_gap_area or is_less_than_min_gap_area:
                current_fitment = Fitment.HORIZONTAL_SCROLL

                # for bellow min image is fitted by width
                if is_less_than_min_gap_area:
                    resize_height = screen_height
                    use_inner_border = False
                    full_screen = True

                # for above max fitment width is screen width minus the maximum allowed amount of gap area
                elif is_more_than_max_gap_area:
                    resize_height = screen_height * (1.0 - self.settings.wide_edge_max)

                resize_width = resize_height * image_ratio
                end_position = resize_width - screen_width

        image_fitment = ImageFitment(self.screen_dimensions)
        image_fitment.end_position = end_position
        image_fitment.current_fitment = current_fitment
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