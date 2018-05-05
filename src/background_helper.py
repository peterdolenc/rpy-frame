from __future__ import division
import pygame
from typing import List, Tuple
import matplotlib, math, scipy, random, os
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
from matplotlib import patches

'''
Functions to define all polygons used in each pattern.
If something is breaking it is most likely addShape().
You must pass a very specific list to this function as described below.
'''

ar = scipy.array


def Rotate2D(pts, cnt, ang=scipy.pi / 4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return scipy.dot(pts - cnt, ar([[scipy.cos(ang), scipy.sin(ang)],
                                    [-scipy.sin(ang), scipy.cos(ang)]])) + cnt


def solveForLeg(h, leg1):
    '''pythagorean theorum to solve for leg (not hypotenuse)'''
    return (math.sqrt(h * h - leg1 * leg1))


def addShape(points, degrees=0, alphaParam=1, ec='none', l=0, jn='round'):
    '''Finalize rotation and add shape to plot.'''
    # "points" should consist of the list returned from any of the
    # geometry functions below (side3, side4, etc.)
    origin = points[-2]
    color = points[-1]
    newPoints = list(points)
    del newPoints[-1]
    del newPoints[-1]

    pts = ar(newPoints)
    radians = degrees * scipy.pi / 180
    ots = Rotate2D(pts, ar([origin]), radians)
    sub1.add_patch(patches.Polygon(ots, fc=color, ec=ec,
                                   alpha=alphaParam, joinstyle=jn, lw=l, rasterized=True))


def side3(w, oX, oY, c, e=0):
    '''Makes a polygon with 3 sides of length w, centered around the origin'''
    base = solveForLeg(w, w / float(2))
    p1 = [oX + w / float(2), oY - ((1 / float(3)) * base)]
    p2 = [oX, oY + (2 / float(3)) * base]
    p3 = [oX - w / float(2), oY - ((1 / float(3)) * base)]
    return ([p1, p2, p3, [oX, oY], c])


def side4(w, oX, oY, c, e=0):
    '''Makes a polygon with 4 sides of length w, centered around the origin.'''
    p1 = [oX - w / float(2), oY - w / float(2)]
    p2 = [oX - (w - e) / float(2), oY + (w - e) / float(2)]
    p3 = [oX + w / float(2), oY + w / float(2)]
    p4 = [oX + (w - e) / float(2), oY - (w - e) / float(2)]
    return ([p1, p2, p3, p4, [oX, oY], c])


def side6(w, oX, oY, c, e=0):
    '''Makes a polygon with 6 sides of length w, centered around the origin.'''
    d = solveForLeg(w, w / float(2))
    de = solveForLeg(w - e, (w - e) / float(2))
    p1 = [oX, oY + w]
    p2 = [oX + de, oY + (w - e) / float(2)]
    p3 = [oX + d, oY - w / float(2)]
    p4 = [oX, oY - (w - e)]
    p5 = [oX - d, oY - w / float(2)]
    p6 = [oX - de, oY + (w - e) / float(2)]
    return ([p1, p2, p3, p4, p5, p6, [oX, oY], c])


def side8(w, oX, oY, c, e=0):
    '''Makes a polygon with 8 sides of length w, centered around the origin.'''
    pts = side4(math.sqrt(2) * w, oX, oY, c)
    pts2 = side4(math.sqrt(2) * w - e, oX, oY, c)
    del pts2[-1]
    del pts2[-1]
    ots = Rotate2D(pts2, ar([oX, oY]), 45 * scipy.pi / 180).tolist()
    return ([pts[0], ots[0], pts[3], ots[3], pts[2],
             ots[2], pts[1], ots[1], [oX, oY], c])


def side12(w, oX, oY, c, e=0):
    '''Makes a polygon with 12 sides, centered around the origin.'''
    # w is not the side length for this function
    pts = side6(w, oX, oY, c)
    pts2 = side6(w - e, oX, oY, c)
    del pts2[-1]
    del pts2[-1]
    ots = Rotate2D(pts2, ar([oX, oY]), 30 * scipy.pi / 180).tolist()
    return ([pts[0], ots[0], pts[5], ots[5], pts[4], ots[4],
             pts[3], ots[3], pts[2], ots[2], pts[1], ots[1], [oX, oY], c])


# diamond functions are for the box pattern only
def diamondA(w, oX, oY, c='#000000', e=0):
    d = math.sqrt(w * w - ((w / float(2)) * (w / float(2))))
    p1 = [oX, oY]
    p2 = [oX, oY + w - e]
    p3 = [oX - d, oY + w - e + (w / float(2))]
    p4 = [oX - d, oY + (w / float(2))]
    return ([p1, p2, p3, p4, [oX, oY], c])


def diamondB(w, oX, oY, c='#000000', e=0):
    d = math.sqrt(w * w - ((w / float(2)) * (w / float(2))))
    p1 = [oX, oY]
    p2 = [oX, oY + w - e]
    p3 = [oX + d, oY + w - e + (w / float(2))]
    p4 = [oX + d, oY + (w / float(2))]
    return ([p1, p2, p3, p4, [oX, oY], c])


def diamondC(w, oX, oY, c='#000000', e=0):
    d = math.sqrt(w * w - ((w / float(2)) * (w / float(2))))
    p1 = [oX, oY + e]
    p2 = [oX, oY + w]
    p3 = [oX - d, oY + w + (w / float(2))]
    p4 = [oX - d, oY + (w / float(2)) + e]
    return ([p1, p2, p3, p4, [oX, oY], c])


def diamondD(w, oX, oY, c='#000000', e=0):
    d = math.sqrt(w * w - ((w / float(2)) * (w / float(2))))
    p1 = [oX, oY + e]
    p2 = [oX, oY + w]
    p3 = [oX + d, oY + w + (w / float(2))]
    p4 = [oX + d, oY + (w / float(2)) + e]
    return ([p1, p2, p3, p4, [oX, oY], c])


def circleSize(c1, c2, c3, c4, c5, width, height):
    '''Pattern 3: Circle Size'''
    global fig
    global sub1 # allow other functions to add shapes to the plot

    fig = plt.figure(figsize=(10,10), dpi=int(width/10+1))
    plt.subplots_adjust(hspace=0, wspace=0)

    ff = [[c5, c2, c4, c2, c5, c1, c5],[c2, c4, c1, c4, c2, c5, c2],
          [c4, c1, c1, c1, c4, c2, c4],[c2, c4, c1, c4, c2, c5, c2],
          [c5, c2, c4, c2, c5, c1, c5],[c1, c5, c2, c5, c1, c1, c1],
          [c5, c2, c4, c2, c5, c1, c5]]

    f2 = [[c4, c1, c5, c1, c4, c2, c4],[c1, c5, c2, c5, c1, c4, c1],
          [c5, c2, c2, c2, c5, c1, c5],[c1, c5, c2, c5, c1, c4, c1],
          [c4, c1, c5, c1, c4, c2, c4],[c2, c4, c1, c4, c2, c2, c2],
          [c4, c1, c5, c1, c4, c2, c4]]

    aa = [[c1, c5, c2, c2, c5, c1, c1],[c5, c2, c4, c4, c2, c5, c5],
          [c2, c4, c1, c1, c4, c2, c2],[c2, c4, c1, c1, c4, c2, c2],
          [c5, c2, c4, c4, c2, c5, c5],[c1, c5, c2, c2, c5, c1, c1],
          [c1, c5, c2, c2, c5, c1, c1]]

    rr = [10, 10, 10, 10, 15, 20, 25, 30, 30, 30, 25, 20, 15]

    rrx = random.randint(0, len(rr)-1)

    sub1 = fig.add_axes((0,0,1,1))
    sub1.xaxis.set_visible(False)
    sub1.yaxis.set_visible(False)
    sub1.set_xlim([0, 480])
    sub1.set_ylim([0, 480])
    sub1.axis('off')
    alpha = 0.5
    for x in range(0, 8):
        for y in range (0, 8):
            xofs = x * 70
            yofs = y * 70
            sub1.add_patch(patches.Rectangle((xofs, yofs), 70, 70, fc=(0.5, 0.5, 0.5), alpha=1, ec='none'))
            sub1.add_patch(patches.Rectangle((xofs, yofs), 70, 70, fc=c3, alpha=alpha, ec='none'))
            for i in range(0, len(ff)):
                count = 1
                for a in range(0, len(ff[0])):
                    sub1.add_patch(patches.Circle((5*count + xofs, 5+2*5*i + yofs), 5, fc=ff[i][a], alpha=alpha, ec='none'))
                    sub1.add_patch(patches.Circle((5*count + xofs, 5+2*5*i + yofs), 3.5, fc=f2[i][a], alpha=random.randint(75, 100)/float(100) * alpha, ec='none'))
                    sub1.add_patch(patches.Circle((5*count-5 + xofs, 2*5*i + yofs),1.5, fc=aa[i][a], alpha=0.75 * alpha, ec='none'))
                    sub1.add_patch(patches.Circle((5*count + xofs, 5+2*5*i + yofs), random.randint(10, rr[rrx])/float(10), fc=c3, alpha=random.randint(50, 85)/float(100) * alpha, ec='none'))
                    sub1.add_patch(patches.Circle((5*count + xofs, 5+2*5*i + yofs), 1, fc=c3, alpha=alpha, ec='none'))
                    count = count + 2

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()

    # Create pygame surface from string
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    plt.clf()


    plt.close('all')

    return surf


def to_hex(rgb):
    rgb = tuple([ int(rgb[i]) for i in range (0, len(rgb)) ])
    return '#%02x%02x%02x' % rgb


class BackgroundHelper:

    def __init__(self, display_mode: List[int]):
        self.display_mode = display_mode

    def get_dominant_color_fill(self, colors: List[Tuple[int]]) -> pygame.Surface:
        surface = pygame.Surface(self.display_mode)
        surface.fill(colors[0])
        return surface

    def get_dominant_pattern(self, colors: List[Tuple[int]]) -> pygame.Surface:
        surface = circleSize(to_hex(colors[0]), to_hex(colors[1]), to_hex(colors[2]), to_hex(colors[3]), to_hex(colors[4]), self.display_mode[0], self.display_mode[1])

        return surface


