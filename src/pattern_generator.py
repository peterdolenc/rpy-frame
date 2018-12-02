import math
import pygame
from typing import List
import scipy
import random
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
from matplotlib import patches

'''
 Idea and base for the code taken from: https://github.com/eleanorlutz/AnimatedPythonPatterns/blob/master/PatternMaker.ipynb
 But quite heavily modified
 Might be replaced in the future by pure surfaces solution instead of plotting
'''
ar = scipy.array


class PatternGenerator:

    def __init__(self, display_mode: List[int]):
        self.display_mode = display_mode

    # creates tne subplot on the figure that has no spacing around
    @staticmethod
    def create_subplot(fig, range_x, range_y, background_color, alpha, gray_lightness):
        subplot = fig.add_axes((0, 0, 1, 1))
        subplot.xaxis.set_visible(False)
        subplot.yaxis.set_visible(False)
        subplot.set_xlim([0, range_x])
        subplot.set_ylim([0, range_y])
        subplot.axis('off')
        neutral_gray = (gray_lightness, gray_lightness, gray_lightness)
        subplot.add_patch(patches.Rectangle((0, 0), range_x, range_y, fc=neutral_gray, alpha=1, ec='none'))
        subplot.add_patch(patches.Rectangle((0, 0), range_x, range_y, fc=background_color, alpha=alpha, ec='none'))
        return subplot

    # converts the plot to a pygame surface
    @staticmethod
    def surface_from_plot(fig):
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        return surf

    # returns a random float in the range
    @staticmethod
    def randf(min, max):
        return random.random() * (max-min) + min

    # Displays different sized circles
    def playful_circles(self, C, B, A, D, E, animation=None, ppi=180, alpha=0.5, background_lightness=0.5, amount_min=0, amount_max=1):

        N = 0x0000001
        rep_size = 60
        circle_radius = 5
        alpha2 = 1.0

        alpha_rand1 = self.randf(0.75, 1.0)
        alpha_rand2 = self.randf(0.5, 0.85)
        amount = self.randf(amount_min, amount_max)

        horizontal_reps = int(math.ceil(float(self.display_mode[0])/float(ppi)))
        vertical_reps = int(math.ceil(float(self.display_mode[1])/float(ppi)))

        fig = plt.figure(figsize=(horizontal_reps, vertical_reps), dpi=ppi)
        plt.subplots_adjust(hspace=0, wspace=0)

        outer_ring_colors = [
            [E, B, D, B, E, A, E],
            [B, D, A, D, B, E, B],
            [D, A, A, A, D, B, D],
            [B, D, A, D, B, E, B],
            [E, B, D, B, E, A, E],
            [A, E, B, E, A, A, A],
            [E, B, D, B, E, A, E]]

        middle_ring_colors = [
            [D, A, E, A, D, B, D],
            [A, E, B, E, A, D, A],
            [E, B, B, B, E, A, E],
            [A, E, B, E, A, D, A],
            [D, A, E, A, D, B, D],
            [B, D, A, D, B, B, B],
            [D, A, E, A, D, B, D]]

        gap_dots_colors = [
            [A, E, B, B, E, A, N],
            [E, B, D, D, B, E, N],
            [B, D, A, A, D, B, N],
            [B, D, A, A, D, B, N],
            [E, B, D, D, B, E, N],
            [A, E, B, B, E, A, N],
            [N, N, N, N, N, N, N]]

        diagonals = lambda i, j: 1 if i == j else 0
        diagonals2 = lambda i, j: 1 if i == 6-j else 0
        small_diff = lambda i, j: 1 if math.fabs(i - j) < 2 else 0
        cross = lambda i, j: 1 if math.fabs(i - 3) + math.fabs(j - 3) < 2 else 0
        full = lambda i, j: 1

        fn = random.choice([ diagonals, diagonals2, small_diff, cross, full ])
        probabilities = [ [  fn(i, j) for j in range(0, 7) ] for i in range(0, 7)]

        # inner dot radius - progression for animation inf enabled
        inner_dot_radiuses = [0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6, 0.6, 0.5, 0.4, 0.3]

        # If animation is enabled create a continuous inner dot radius value from discrete points above
        if animation is None:
            inner_dot_max_radius = random.choice(inner_dot_radiuses)
        else:
            animation_stages = len(inner_dot_radiuses)  # 12
            accurate_index = min(0.99999, animation) * (animation_stages-1)  # 7.81
            bottom_index = int(accurate_index)  # 0.71 * 11 = 7.81 => 7
            reminder = accurate_index - bottom_index  # 0.81
            top_index = bottom_index + 1  # 8
            inner_dot_max_radius = reminder * inner_dot_radiuses[top_index] + (1-reminder) * inner_dot_radiuses[bottom_index]

        # prepare subplot
        background_color = C
        subplot = self.create_subplot(fig, horizontal_reps * rep_size, vertical_reps * rep_size, background_color, alpha, background_lightness)

        for h_rep in range(0, horizontal_reps):
            for v_rep in range(0, vertical_reps):
                offset_x = h_rep * rep_size
                offset_y = v_rep * rep_size

                # i goes from 0 to number of color sets in ff (7) - rows
                for i in range(0, len(outer_ring_colors)):

                    # j goes from 0 to number of colors in every set (7) - columns
                    for j in range(0, len(outer_ring_colors[0])):

                        if probabilities[i][j] <= amount and self.randf(0, 0.8) <= amount:
                            continue

                        center_x = offset_x + circle_radius * (2*j + 1)
                        center_y = offset_y + circle_radius * (2*i + 1)

                        # outer circle
                        subplot.add_patch(
                            patches.Circle((center_x, center_y), circle_radius, fc=outer_ring_colors[i][j], alpha=alpha*alpha2, ec='none'))

                        # middle circle
                        subplot.add_patch(
                            patches.Circle((center_x, center_y), 0.7 * circle_radius, fc=middle_ring_colors[i][j], alpha=alpha_rand1*alpha*alpha2, ec='none'))

                        # small circle in the gap between
                        if gap_dots_colors[i][j] != N:
                            subplot.add_patch(
                                patches.Circle((center_x - circle_radius, center_y - circle_radius), 0.3*circle_radius, fc=gap_dots_colors[i][j], alpha=0.75*alpha*alpha2, ec='none'))

                        # slightly less opaque random growing dot surround
                        subplot.add_patch(
                            patches.Circle((center_x, center_y), self.randf(0.2, inner_dot_max_radius) * circle_radius, fc=background_color, alpha=alpha_rand2 * alpha*alpha2, ec='none'))

                        # the dot
                        subplot.add_patch(
                            patches.Circle((center_x, center_y), 0.2*circle_radius, fc=background_color, alpha=alpha, ec='none'))

        # create surface from plot and clean the plot
        surf = self.surface_from_plot(fig)
        plt.clf()
        plt.close('all')

        return surf
