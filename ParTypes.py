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

    def construct(self, start, end):
        self.__init__(start, end)

    def length(self):
        return math.sqrt(np.sum(self.to_vec2d() ** 2))

    def to_vec2d(self):
        return self.end.to_vec2d() - self.start.to_vec2d()

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

    def render(self, ax, scaling):
        self.mobject.scale(scaling / 4)
        self.mobject.align_to(ax.c2p(self.point.x, self.point.y), DOWN + LEFT)
        return self

    def spread_vertices(self):
        vertices = []
        offset = self.vertices[0]
        for v in self.vertices:
            new_v = v - offset
            vertices.append(MyPoint(new_v.x * 10, new_v.y * 10))
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


class Tiling:
    def __init__(self):
        self.mobject = Rectangle(WHITE, 0, 0)

    def union(self, rect):
        self.mobject = Union(self.mobject, rect)
