from typing import List, Tuple
import colorsys
import pygame
from colorthief import ColorThief

from entities.image_meta import ImageMeta


class ImageHelper:

    def resize(image: pygame.Surface,  dimensions) -> pygame.Surface:
        dimensions = (int(dimensions[0]), int(dimensions[1]))
        return pygame.transform.smoothscale(image, dimensions)

    def get_dominant_colors(image_meta: ImageMeta, image:pygame.Surface, color_thief=True) -> List[Tuple[int]]:
        if color_thief:
            ct = ColorThief(image_meta.full_path)
            colors = ct.get_palette(10, 10)
            hsvs = [ (*colorsys.rgb_to_hsv(*colors[i]), i) for i in range(len(colors)) ]
            hsvs.sort(key=lambda c: ImageHelper.grade_color(*c), reverse=True)
            rgbs = [ colorsys.hsv_to_rgb(c[0], c[1], c[2]) for c in hsvs]
            return rgbs
        else:
            pixarray = pygame.PixelArray(image)
            colors = []
            color_steps = 6
            color_gap = int(256.0 / float(color_steps) + 0.5)

            for i in range(pixarray.shape[0]):
                if (i % 3 == 0):
                    for j in range(pixarray.shape[1]):
                        if (j % 3 == 0):
                            # rgbc = pygame.Color(pixarray[i,j]*256 + 255)
                            pixel = image.get_at((i, j))
                            r = pixel[0]
                            g = pixel[1]
                            b = pixel[2]
                            colorint = r / color_gap * color_steps * color_steps + g / color_gap * color_steps + b / color_gap
                            colors.append(colorint)

            fcolor = ImageHelper.most_common(colors)

            dominant_color = pygame.Color(((fcolor / color_steps / color_steps) % color_steps) * color_gap + color_gap / 2,
                                          ((fcolor / color_steps) % color_steps) * color_gap + color_gap / 2, ((fcolor) % color_steps) * color_gap + color_gap / 2, 255)

            return [ dominant_color ]

    def most_common(lst: List):
        return max(set(lst), key=lst.count)

    def grade_color(h, s ,v, i):
        v = float(v) / 256
        if s < 0.1 or v < 0.1 or s + v < 0.3:
            return 0
        return (2 * pow(s, 3) + pow(v, 3)) * (3 ** (1/(i+1)))
