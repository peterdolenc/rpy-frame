from typing import List, Tuple
import colorsys
import pygame
import fast_colorthief

from entities.image_meta import ImageMeta


class DominantColorExtractor:

    # gets the dominant colors
    # uses color thief to extract them
    # then sorts them by color intensity and occurrence
    def get_dominant_colors(
        image_meta: ImageMeta,
        image: pygame.Surface,
        colour_count=8,
    ) -> List[Tuple[int]]:
        colors = fast_colorthief.get_palette(image_meta.full_path)
        hsvs = [(*colorsys.rgb_to_hsv(*colors[i]), i) for i in range(len(colors))]
        hsvs.sort(key=lambda c: DominantColorExtractor.grade_color(*c), reverse=True)
        rgbs = [colorsys.hsv_to_rgb(c[0], c[1], c[2]) for c in hsvs]
        return rgbs

    # grades a HSV color with occurrence i
    # if the color is very dark or very washed out then score is zero
    # otherwise its a combination of intensity and saturation and occurrence
    def grade_color(h, s, v, i):
        if i == 0:
            return 99999999999999999
        v = float(v) / 256
        if s < 0.05 or v < 0.05 or s + v < 0.2:
            return 0
        return (2 * pow(s, 2) + pow(v, 2)) * (4 ** (1 / (i + 1)))
