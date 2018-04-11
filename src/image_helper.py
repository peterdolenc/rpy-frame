from typing import List, Tuple
import colorsys
import pygame
from colorthief import ColorThief

from entities.image_meta import ImageMeta


class ImageHelper:

    # resizes the image to target dimensions
    def resize(image: pygame.Surface,  dimensions) -> pygame.Surface:
        dimensions = (int(dimensions[0]), int(dimensions[1]))
        return pygame.transform.smoothscale(image, dimensions)

    # gets the dominant colors
    # uses color thief to extract them
    # then sorts them by color intensity and occurrence
    def get_dominant_colors(image_meta: ImageMeta, image:pygame.Surface, colour_count=10, sampling=10) -> List[Tuple[int]]:
        ct = ColorThief(image_meta.full_path)
        colors = ct.get_palette(colour_count, sampling)
        hsvs = [ (*colorsys.rgb_to_hsv(*colors[i]), i) for i in range(len(colors)) ]
        hsvs.sort(key=lambda c: ImageHelper.grade_color(*c), reverse=True)
        rgbs = [ colorsys.hsv_to_rgb(c[0], c[1], c[2]) for c in hsvs]
        return rgbs

    # grades a HSV color with occurrence i
    # if the color is very dark or very washed out then score is zero
    # otherwise its a combination of intensity and saturation and occurrence
    def grade_color(h, s ,v, i):
        v = float(v) / 256
        if s < 0.1 or v < 0.1 or s + v < 0.3:
            return 0
        return (2 * pow(s, 3) + pow(v, 3)) * (3 ** (1/(i+1)))
