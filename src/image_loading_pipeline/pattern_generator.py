import math
import random
from typing import List
import matplotlib
import numpy as np
import pygame
matplotlib.use('Agg')
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image, ImageFilter

'''
 Idea and base for the code taken from: https://github.com/eleanorlutz/AnimatedPythonPatterns/blob/master/PatternMaker.ipynb
 But quite heavily modified
 Might be replaced in the future by pure surfaces solution instead of plotting
'''

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
    def surface_from_plot(fig, blur, blur_radius):
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        if blur:
            img = Image.frombytes("RGB", size, raw_data)
            blur = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            raw_data = blur.tobytes()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        return surf

    # returns a random float in the range
    @staticmethod
    def randf(min, max):
        return random.random() * (max-min) + min

    # Displays different sized circles
    def playful_circles(self, C, B, A, D, E, animation=None, ppi=180, alpha=0.5, background_lightness=0.5, amount_min=0, amount_max=1, blur=True, blur_radius=2):

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
        surf = self.surface_from_plot(fig, blur, blur_radius)
        plt.clf()
        plt.close('all')

        return surf

    @staticmethod
    def Rotate2D(pts, cnt, ang=np.pi / 4):
        '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
        return np.dot(pts - cnt, np.array([[np.cos(ang), np.sin(ang)],
                                        [-np.sin(ang), np.cos(ang)]])) + cnt

    @staticmethod
    def solveForLeg(h, leg1):
        '''pythagorean theorum to solve for leg (not hypotenuse)'''
        return (math.sqrt(h * h - leg1 * leg1))

    @staticmethod
    def side3(w, oX, oY, c, e=0):
        '''Makes a polygon with 3 sides of length w, centered around the origin'''
        base = PatternGenerator.solveForLeg(w, w / float(2))
        p1 = [oX + w / float(2), oY - ((1 / float(3)) * base)]
        p2 = [oX, oY + (2 / float(3)) * base]
        p3 = [oX - w / float(2), oY - ((1 / float(3)) * base)]
        return ([p1, p2, p3, [oX, oY], c])

    @staticmethod
    def side4(w, oX, oY, c, e=0):
        '''Makes a polygon with 4 sides of length w, centered around the origin.'''
        p1 = [oX - w / float(2), oY - w / float(2)]
        p2 = [oX - (w - e) / float(2), oY + (w - e) / float(2)]
        p3 = [oX + w / float(2), oY + w / float(2)]
        p4 = [oX + (w - e) / float(2), oY - (w - e) / float(2)]
        return ([p1, p2, p3, p4, [oX, oY], c])

    @staticmethod
    def side6(w, oX, oY, c, e=0):
        '''Makes a polygon with 6 sides of length w, centered around the origin.'''
        d = PatternGenerator.solveForLeg(w, w / float(2))
        de = PatternGenerator.solveForLeg(w - e, (w - e) / float(2))
        p1 = [oX, oY + w]
        p2 = [oX + de, oY + (w - e) / float(2)]
        p3 = [oX + d, oY - w / float(2)]
        p4 = [oX, oY - (w - e)]
        p5 = [oX - d, oY - w / float(2)]
        p6 = [oX - de, oY + (w - e) / float(2)]
        return ([p1, p2, p3, p4, p5, p6, [oX, oY], c])

    @staticmethod
    def side8(w, oX, oY, c, e=0):
        '''Makes a polygon with 8 sides of length w, centered around the origin.'''
        pts = PatternGenerator.side4(math.sqrt(2) * w, oX, oY, c)
        pts2 = PatternGenerator.side4(math.sqrt(2) * w - e, oX, oY, c)
        del pts2[-1]
        del pts2[-1]
        ots = PatternGenerator.Rotate2D(pts2, np.array([oX, oY]), 45 * np.pi / 180).tolist()
        return ([pts[0], ots[0], pts[3], ots[3], pts[2],
                 ots[2], pts[1], ots[1], [oX, oY], c])

    @staticmethod
    def side12(w, oX, oY, c, e=0):
        '''Makes a polygon with 12 sides, centered around the origin.'''
        # w is not the side length for this function
        pts = PatternGenerator.side6(w, oX, oY, c)
        pts2 = PatternGenerator.side6(w - e, oX, oY, c)
        del pts2[-1]
        del pts2[-1]
        ots = PatternGenerator.Rotate2D(pts2, np.array([oX, oY]), 30 * np.pi / 180).tolist()
        return ([pts[0], ots[0], pts[5], ots[5], pts[4], ots[4],
                 pts[3], ots[3], pts[2], ots[2], pts[1], ots[1], [oX, oY], c])

    @staticmethod
    def addShape(sub1, cx, cy, points, degrees=0, alphaParam=1, ec='none', l=0, jn='round'):
        '''Finalize rotation and add shape to plot.'''
        # "points" should consist of the list returned from any of the
        # geometry functions below (side3, side4, etc.)
        origin = points[-2]
        color = points[-1]
        newPoints = list(points)
        del newPoints[-1]
        del newPoints[-1]

        pts = np.array(newPoints)
        radians = degrees * np.pi / 180
        origin = (origin[0] + cx, origin[1]+cy)

        pts2 = [(p[0] + cx, p[1] +cy) for p in pts]
        ots = PatternGenerator.Rotate2D(pts2, np.array([origin]), radians)

        sub1.add_patch(patches.Polygon(ots, fc=color, ec=ec,
                                       alpha=alphaParam, joinstyle=jn, lw=l, rasterized=True))

    # astro stars animation
    def astro_stars(self, C, B, A, D, E, animation=None, ppi=180, alpha=0.5, background_lightness=0.5, amount_min=0, amount_max=1, blur=True, blur_radius=2):

        rep_size = 91
        rep_size_v = 52
        ppi = int(ppi/1.5)

        alpha_rand1 = self.randf(0.75, 1.0)*alpha
        alpha_rand2 = self.randf(0.5, 0.85)*alpha
        amount = self.randf(amount_min, amount_max)

        horizontal_reps = int(math.ceil(float(self.display_mode[0]) / float(ppi) * rep_size / rep_size_v))
        vertical_reps = int(math.ceil(float(self.display_mode[1]) / float(ppi)))

        fig = plt.figure(figsize=(math.ceil(horizontal_reps* rep_size / rep_size_v), vertical_reps), dpi=ppi)
        plt.subplots_adjust(hspace=0, wspace=0)


        diagonals = lambda i, j: 1 if i == j else 0
        diagonals2 = lambda i, j: 1 if i == 6 - j else 0
        small_diff = lambda i, j: 1 if math.fabs(i - j) < 2 else 0
        cross = lambda i, j: 1 if math.fabs(i - 3) + math.fabs(j - 3) < 2 else 0
        full = lambda i, j: 1

        fn = random.choice([diagonals, diagonals2, small_diff, cross, full])
        probabilities = [[fn(i, j) for j in range(0, horizontal_reps)] for i in range(0, vertical_reps)]


        # origin locations plus rotation angle for each shape set
        base_shapes = [[19.75, 50, -90], [80.25, 50, 90], [35, 24, 90], [65, 24, -90],
              [65, 76, -90], [35, 76, 90]]
        main_star_origins = [[50, 50, E, D], [4.5, 24, D, E], [4.5, 76, D, E], [95.5, 76, D, E],
               [95.5, 24, D, E], [50, 102, E, D], [50, -2, E, D]]
        mini_triangles = [[23, 55.65, -90], [77, 55.66, 90], [31.75, 29.65, 90],
               [68.25, 29.65, -90], [23, 44.45, -90], [77, 44.45, 90],
               [68.25, 70.45, -90], [31.75, 70.45, 90], [13.39, 50, -90],
               [86.71, 50, 90], [41.5, 24, 90], [58.45, 24, -90],
               [58.45, 76, -90], [41.5, 76, 90]]

        # diff of star rays (how big are rays compared to star bodies) for various shapes
        lhex = [-2, -1, 0, 2, 4, 7, 7, 7, 4, 2, 0, -1]
        lstar = [12, 11, 10, 8, 6, 3, 3, 3, 6, 8, 10, 11]
        lin2 = [-1, -2, -3, -5, -7, -9, -7, -9, -7, -5, -3, -2]
        linner = [-6, -7, -8, -6, -4, -3, -1, -3, -4, -6, -8, -7]

        # opacities
        opacities = [a*alpha for a in [0.75, 0.7, 0.6, 0.5, 0.45, 0.4, 0.4, 0.4, 0.45, 0.5, 0.6, 0.7]]
        opacities2 = [a*alpha for a in [0.75, 0.8, 0.85, 0.95, 1, 1, 1, 1, 1, 0.95, 0.85, 0.8]]


        # main star dimensions
        main_star_dimensions1 = [6.35, 6.6, 7, 9.5, 13.5, 18, 19.5, 18, 13.5, 9.5, 7, 6.6]
        main_star_dimensions2 = [3, 3.5, 4, 5.5, 7, 9, 12, 9, 7, 5.5, 4, 3.5]
        main_star_dimensions3 = [2, 2.5, 3, 4, 5, 6.5, 8, 6.5, 5, 4, 3, 2.5]

        # If animation is enabled then animate by steps
        if animation is None:
            x = random.randint(0, len(opacities2) - 1)
        else:
            animation_stages = len(opacities2)
            accurate_index = min(0.99999, animation) * (animation_stages - 1)
            bottom_index = int(accurate_index)
            x = bottom_index

        # prepare subplot
        background_color = C
        subplot = self.create_subplot(fig, horizontal_reps * rep_size, vertical_reps * rep_size_v, background_color, alpha, background_lightness)

        # iterate through vertical and horizontal repetitions of subplots
        for h_rep in range(0, horizontal_reps):
            for v_rep in range(0, vertical_reps):
                offset_x = h_rep * rep_size
                offset_y = v_rep * rep_size_v

                if probabilities[v_rep][h_rep] <= amount and self.randf(0, 0.8) <= amount:
                   continue

                # Base triangles and hexes
                for n in range(0, len(base_shapes)):
                    pts = self.side3(11, base_shapes[n][0], base_shapes[n][1], E, 2)
                    pts2 = self.side6(13, base_shapes[n][0], base_shapes[n][1], B, lhex[x])
                    pts3 = self.side3(22.5, base_shapes[n][0], base_shapes[n][1], C)
                    pts4 = self.side3(5.5, base_shapes[n][0], base_shapes[n][1], A)
                    self.addShape(subplot, offset_x, offset_y, pts2, base_shapes[n][2] / (3), alphaParam=alpha_rand1)
                    self.addShape(subplot, offset_x, offset_y, pts3, base_shapes[n][2] / (3), alphaParam=alpha_rand1)
                    self.addShape(subplot, offset_x, offset_y, pts, base_shapes[n][2], alphaParam=alpha_rand1)
                    self.addShape(subplot, offset_x, offset_y, pts4, base_shapes[n][2] * -1, alpha)

                # Mini triangles around the center
                for n in range(0, len(mini_triangles)):
                    pts = self.side3(5.5, mini_triangles[n][0], mini_triangles[n][1], A)
                    self.addShape(subplot, offset_x, offset_y, pts, mini_triangles[n][2], opacities[x])

                # Hex stars and overlapped circles
                for n in range(0, len(main_star_origins)):
                    c = plt.Circle((main_star_origins[n][0] + offset_x, main_star_origins[n][1] + offset_y), radius=3.5, color=A, alpha=alpha)
                    pts = self.side12(24, main_star_origins[n][0], main_star_origins[n][1], main_star_origins[n][2], lstar[x])
                    pts2 = self.side12(main_star_dimensions1[x], main_star_origins[n][0], main_star_origins[n][1], main_star_origins[n][3], linner[x])
                    pts3 = self.side12(main_star_dimensions2[x], main_star_origins[n][0], main_star_origins[n][1], A, lin2[x])
                    pts4 = self.side12(main_star_dimensions3[x], main_star_origins[n][0], main_star_origins[n][1], main_star_origins[n][2], lin2[x] - 6)
                    self.addShape(subplot, offset_x, offset_y, pts, alphaParam=alpha_rand2)
                    self.addShape(subplot, offset_x, offset_y, pts2, 0, min(1, opacities[x] + 0.25)*alpha)
                    self.addShape(subplot, offset_x, offset_y, pts3, -30, alphaParam=alpha_rand2)
                    self.addShape(subplot, offset_x, offset_y, pts4, 0, opacities2[x])
                    subplot.add_artist(c)

        # create surface from plot and clean the plot
        surf = self.surface_from_plot(fig, blur, blur_radius)
        plt.clf()
        plt.close('all')

        return surf