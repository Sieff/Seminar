import math

import numpy as np

from MyMath import *
from manim import *
from decimal import *

import random

#seed = 723637645
seed = random.randrange(sys.maxsize)
random.seed(seed)
print("Seed was:", seed)

getcontext().prec = 6


def vertices_as_sequence(v):
    result = []
    for i in v:
        result.append(i.to_vec3d())
    return result


class BaseRectangle:
    def __init__(self, width=1, height=1, init_points_type='RANDOM', num_points=5, points=[]):
        self.height = height
        self.width = width
        self.pointsSet = {MyPoint(0, 0)}
        self.mobject = Rectangle(WHITE, width, height)
        self.beta_tile_index = -1
        self._init_points(init_points_type, num_points, points)
        self.label = Tex('$U$').next_to(self.mobject, UP + RIGHT, buff=0.1)

    def _init_points(self, type, num_points, points):
        if type == 'RANDOM':
            for i in range(num_points):
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
                self.add_point(x, y)
        elif type == 'CUSTOM':
            for point in points:
                self.add_point(point.x, point.y)
        elif type == 'DIAGONAL':
            for i in range(0, num_points):
                self.add_point(i * 1 / num_points, i * 1 / num_points)
        elif type == 'BETA':
            self.add_point(0.5, 0.5)
            self.add_point(0.5, 0.6)
            self.add_point(0.6, 0.5)
            self.add_point(0.513, 0.591)
            self.add_point(0.516, 0.565)
            self.add_point(0.519, 0.545)
            self.add_point(0.531, 0.526)
            self.add_point(0.547, 0.519)
            self.add_point(0.559, 0.517)
            self.add_point(0.583, 0.513)
        elif type == 'WIDE':
            self.add_point(0.5, 0.5)
            self.add_point(0.5, 0.6)
            self.add_point(0.7, 0.5)
            self.add_point(0.503, 0.591)
            self.add_point(0.505, 0.565)
            self.add_point(0.507, 0.545)
            self.add_point(0.51, 0.526)
            self.add_point(0.515, 0.517)
            self.add_point(0.52, 0.505)
            self.add_point(0.599, 0.503)
        elif type == 'GREEDYBETTER':
            self.add_point(0.7, 0.75)
            self.add_point(0.35, 0.65)
            self.add_point(0.8, 0.1)
        elif type == 'INTRO':
            self.add_point(0.2, 0.3)
            self.add_point(0.5, 0.2)
            self.add_point(0.4, 0.6)
            self.add_point(0.8, 0.4)
            self.add_point(0.7, 0.9)

    def add_point(self, x, y):
        if 1 >= x >= 0 and 1 >= y >= 0:
            self.pointsSet.add(MyPoint(x, y))
            self.beta_tile_index = self.beta_tile_index + 1

    def render(self, ax, scaling):
        self.mobject.scale(scaling)
        self.mobject.move_to(ax.c2p(0, 0, 0))
        self.mobject.shift(UP * scaling * (self.height / 2), RIGHT * scaling * (self.width / 2))
        self.label.next_to(self.mobject, UP + RIGHT, buff=0.1)


class MyPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mobject = Dot(radius=0.05, color=BLUE)

    def construct(self, x, y):
        self.__init__(x, y)

    def render(self, ax):
        self.mobject.move_to(ax.c2p(self.x, self.y, 0))
        return self

    def to_vec2d(self):
        return np.array([self.x, self.y])

    def as_coordinates(self):
        return [self.x, self.y, 0]

    def to_vec3d(self):
        return np.array([self.x * 2, self.y * 2, 0])

    def __eq__(self, other):
        quantizer = '1.00000'
        margin = 0.000001
        return Decimal(str(self.x + margin)).quantize(Decimal(quantizer), rounding=ROUND_DOWN) == Decimal(str(other.x + margin)).quantize(
            Decimal(quantizer), rounding=ROUND_DOWN) and \
               Decimal(str(self.y + margin)).quantize(Decimal(quantizer), rounding=ROUND_DOWN) == Decimal(str(other.y + margin)).quantize(
            Decimal(quantizer), rounding=ROUND_DOWN)

    def __hash__(self):
        return round(self.x * 1000000 + self.y * 1000)

    def __str__(self):
        return 'X: ' + str(self.x) + ', Y: ' + str(self.y)

    def __repr__(self):
        return '<MyPoint: ' + self.__str__() + '>'

    def __add__(self, other):
        return MyPoint(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return MyPoint(self.x - other.x, self.y - other.y)

class MyLine:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.mobject = Dot()

    def render(self, ax):
        self.mobject = Line(ax.c2p(*self.start.to_vec2d()), ax.c2p(*self.end.to_vec2d()))
        return self

    def length(self):
        return math.sqrt(np.sum(self.to_vec2d() ** 2))

    def to_vec2d(self):
        return self.end.to_vec2d() - self.start.to_vec2d()

    def to_vec3d(self):
        vector = self.end.to_vec2d() - self.start.to_vec2d()
        return np.append(vector, [0])

    def is_orthogonal(self):
        vector_angle = angle(self.to_vec2d(), UP[:2]) % 90
        return vector_angle <= 0.01 or vector_angle >= 89.99

    def intersects(self, other):
        return doIntersect(self.start, self.end, other.start, other.end)

    def _array_eq(self, a, b):
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True

    def parallels(self, other):
        my_o = self.end.to_vec2d() - self.start.to_vec2d() / np.sqrt(
            np.sum((self.end.to_vec2d() - self.start.to_vec2d()) ** 2))
        other_o = other.end.to_vec2d() - other.start.to_vec2d() / np.sqrt(
            np.sum((other.end.to_vec2d() - other.start.to_vec2d()) ** 2))
        return self._array_eq(my_o, other_o) or self._array_eq(my_o, other_o * -1)

    def __str__(self):
        return '    Start: ' + self.start.__str__() + '\n' + \
               '    End: : ' + self.end.__str__()

    def __repr__(self):
        return '<MyLine: \n' \
               + self.__str__() + '>\n'

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return self.start.__hash__() * 1000 + self.end.__hash__()


class MyPolygon:
    def __init__(self, vertices):
        self.vertices = vertices
        self.points = []
        self.mobject = Dot()

    def render(self, ax):
        self.calc_points(ax)
        self.mobject = Polygon(*self.points, color=BLUE, fill_opacity=0.5)
        return self

    def calc_points(self, ax):
        points = []
        for v in self.vertices:
            points.append(ax.c2p(*v.as_coordinates()))
        self.points = points
        return points


class PackedRectangle:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.width = end.x - start.x
        self.height = end.y - start.y
        self.mobject = Rectangle(BLUE, self.height, self.width, fill_opacity= 0.2)
        self.transform_base = Rectangle(BLUE, 0, 0).move_to(start.mobject)

    def construct(self, start, end):
        self.__init__(start, end)

    def render(self, ax, scaling):
        self.mobject.scale(scaling / 2)
        self.mobject.move_to(ax.c2p(self.start.x, self.start.y))
        self.mobject.shift(UP * scaling / 2 * (self.height / 2), RIGHT * scaling / 2 * (self.width / 2))
        return self

    def render_transform_base(self):
        self.transform_base.move_to(self.start.mobject)

    def get_area(self):
        return self.width * self.height


class PossiblePolygon:
    def __init__(self, point, vertices):
        self.point = point
        self.mobject = Polygon(*vertices_as_sequence(vertices), color=GREEN, fill_color=GREEN, fill_opacity=0.4)
        self.vertices = vertices
        self.flipped = False
        self.triangle = Triangle()

    def render(self, ax, scaling):
        self.mobject.scale(scaling / 4)
        self.mobject.align_to(ax.c2p(self.point.x, self.point.y), DOWN + LEFT)
        return self

    def spread_vertices(self, scale):
        vertices = []
        offset = self.vertices[0]
        for v in self.vertices:
            new_v = v - offset
            vertices.append(MyPoint(new_v.x * scale, new_v.y * scale))
        self.vertices = np.array(vertices)
        self.point = self.vertices[0]
        return self.vertices

    def flip_vertices(self):
        self.vertices = np.flip(np.append(self.vertices, self.vertices[0]))[:-1]
        self.flipped = not self.flipped
        return self.vertices

    def coverage(self):
        area = self.get_area()
        max_area = 0
        for i, v in enumerate(self.vertices):
            if i % 2 == 0 or i < 3:
                continue
            rect = PackedRectangle(self.point, v)
            if rect.get_area() > max_area:
                max_area = rect.get_area()
        return max_area / area

    def get_area(self):
        result = 0
        if self.flipped:
            self.flip_vertices()

        for i, v in enumerate(self.vertices):
            if i % 2 == 0 or i < 3:
                continue
            prev = self.vertices[i-1]
            w = prev.x - v.x
            h = v.y
            result = result + w * h
        return result

    def get_tip(self, dir, ax, scaling, beta=5):
        area = self.get_area() / beta
        if dir == 'u':
            self.flip_vertices()
        cum_area = 0
        tip_index = -1
        for i, v in enumerate(self.vertices):
            if i % 2 == 0 or i < 3:
                continue
            prev = self.vertices[i - 1]
            if dir == 'r':
                w = prev.x - v.x
                h = v.y
            else:
                w = prev.y - v.y
                h = v.x
            cum_area = cum_area + w * h
            if cum_area > area:
                tip_index = i
                break
        if dir == 'r':
            start = MyPoint(self.vertices[tip_index].x, 0)
        else:
            start = MyPoint(0, self.vertices[tip_index].y)
        tip = PossiblePolygon(start, np.append(np.array([start]), self.vertices[1:tip_index + 1])).render(ax, scaling)
        if dir == 'u':
            tip.flipped = True
        return tip


class Triangle:
    def __init__(self, factor=1):
        self.vertices = [MyPoint(0, 0), MyPoint(1 * factor, 0), MyPoint(1 * factor, -1 * factor)]
        self.points = vertices_as_sequence(self.vertices)
        self.mobject = Polygon(*self.points, color=BLUE, fill_opacity=0.2)
        self.trapezoid = Dot()

    def render(self, ax):
        new_points = []
        for v in self.vertices:
            new_points.append(ax.c2p(*v.to_vec2d()))
        self.points = new_points
        self.mobject = Polygon(*self.points, color=BLUE, fill_opacity=0.2).align_to(ax.c2p(0), UL)
        return self

    def get_trapezoid(self, _lambda, ai, ax):
        self.trapezoid = Trapezoid(_lambda, ai).render(ax)
        return self.trapezoid


class Trapezoid:
    def __init__(self, _lambda, ai):
        vertices = [MyPoint(0, 0), MyPoint(ai, 0), MyPoint(ai, -(ai * _lambda)), MyPoint((ai * _lambda), -(ai * _lambda))]
        self.vertices = vertices
        self.points = []
        self.mobject = Dot()
        self.label = Tex(r'$A$', font_size=28)

    def render(self, ax):
        points = []
        for v in self.vertices:
            points.append(ax.c2p(*v.to_vec2d()))
        self.points = points
        self.mobject = Polygon(*points, color=RED, fill_opacity=0.2).align_to(ax.c2p(0), UL)
        self.label.move_to(self.mobject.get_center())
        return self

    def set_label(self, index):
        self.label = Tex(r'$A_' + str(index) + r'$', font_size=28).move_to(self.mobject.get_center())

    def get_l_d(self, ax):
        arr = DoubleArrow(start=ax.c2p(*self.vertices[3].as_coordinates()), end=ax.c2p(*MyPoint(0, self.vertices[3].y).as_coordinates()), tip_length=0.1, stroke_width=2, buff=0).align_to(self.mobject, DL).shift(DOWN * 0.2)
        label = Tex(r'$\lambda |a_i^\prime|$', font_size=28).next_to(arr, DOWN, buff=0.08)
        l_divider = Line(ax.c2p(0), ax.c2p(*MyPoint(0, self.vertices[3].y - 0.05).to_vec2d()), stroke_width=1)
        r_divider = Line(ax.c2p(*self.vertices[3].to_vec2d()), ax.c2p(*MyPoint(self.vertices[3].x, self.vertices[3].y - 0.05).to_vec2d()), stroke_width=1)
        return arr, label, l_divider, r_divider

    def get_r_d(self, ax):
        arr = DoubleArrow(start=ax.c2p(*self.vertices[3].as_coordinates()), end=ax.c2p(*self.vertices[2].as_coordinates()), tip_length=0.1, stroke_width=2, buff=0).align_to(self.mobject, DR).shift(DOWN * 0.2)
        label = Tex(r'$(1-\lambda) |a_i^\prime|$', font_size=28).next_to(arr, DOWN, buff=0.08).shift(RIGHT * 0.1)
        l_divider = Line(ax.c2p(*self.vertices[3].to_vec2d()), ax.c2p(*MyPoint(self.vertices[3].x, self.vertices[3].y - 0.05).to_vec2d()), stroke_width=1)
        r_divider = Line(ax.c2p(*self.vertices[2].to_vec2d()), ax.c2p(*MyPoint(self.vertices[2].x, self.vertices[2].y - 0.05).to_vec2d()), stroke_width=1)
        return arr, label, l_divider, r_divider

    def get_r(self, ax):
        arr = DoubleArrow(start=ax.c2p(*self.vertices[2].as_coordinates()), end=ax.c2p(*self.vertices[1].as_coordinates()), tip_length=0.1, stroke_width=2, buff=0).next_to(self.mobject, RIGHT, buff=0.08)
        label = Tex(r'$\lambda |a_i^\prime|$', font_size=28).next_to(arr, RIGHT, buff=0.1)
        divider = Line(ax.c2p(*self.vertices[2].to_vec2d()), ax.c2p(*MyPoint(self.vertices[2].x + 0.05, self.vertices[3].y).to_vec2d()), stroke_width=1)
        return arr, label, divider


class Tiling:
    def __init__(self):
        self.mobject = Rectangle(WHITE, 0, 0)

    def union(self, rect):
        self.mobject = Union(self.mobject, rect)
