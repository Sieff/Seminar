import math

import numpy as np

from MyMath import *
from manim import *
from decimal import *

getcontext().prec = 6


class BaseRectangle:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.pointsSet = {MyPoint(0, 0)}
        self.mobject = Rectangle(WHITE, width, height)

    def construct(self, width=1, height=1):
        self.__init__(width, height)

    def add_point(self, x, y):
        if 1 >= x >= 0 and 1 >= y >= 0:
            self.pointsSet.add(MyPoint(x, y))

    def render(self, ax, scaling):
        self.mobject.scale(scaling)
        self.mobject.move_to(ax.c2p(0, 0, 0))
        self.mobject.shift(UP * scaling * (self.height / 2), RIGHT * scaling * (self.width / 2))


class MyPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mobject = Dot(radius=0.05)

    def construct(self, x, y):
        self.__init__(x, y)

    def render(self, ax):
        self.mobject.move_to(ax.c2p(self.x, self.y, 0))

    def to_vec2d(self):
        return np.array([self.x, self.y])

    def to_vec3d(self):
        return np.array([self.x*2, self.y*2, 0])

    def __eq__(self, other):
        return Decimal(self.x).quantize(Decimal('1.00000'), rounding=ROUND_DOWN) == Decimal(other.x).quantize(Decimal('1.00000'), rounding=ROUND_DOWN) and \
               Decimal(self.y).quantize(Decimal('1.00000'), rounding=ROUND_DOWN) == Decimal(other.y).quantize(Decimal('1.00000'), rounding=ROUND_DOWN)

    def __hash__(self):
        return round(self.x * 1000000 + self.y * 1000)

    def __str__(self):
        return 'X: ' + str(self.x) + ', Y: ' + str(self.y)

    def __repr__(self):
        return '<MyPoint: ' + self.__str__() + '>'


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
        my_o = self.end.to_vec2d() - self.start.to_vec2d() / np.sqrt(np.sum((self.end.to_vec2d() - self.start.to_vec2d())**2))
        other_o = other.end.to_vec2d() - other.start.to_vec2d() / np.sqrt(np.sum((other.end.to_vec2d() - other.start.to_vec2d())**2))
        return self._array_eq(my_o, other_o) or self._array_eq(my_o, other_o * -1)

    def __str__(self):
        return '    Start: ' + self.start.__str__() + '\n' +\
               '    End: : ' + self.end.__str__()

    def __repr__(self):
        return '<MyLine: \n'\
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
        self.mobject = Rectangle(BLUE, self.height, self.width)

    def construct(self, start, end):
        self.__init__(start, end)

    def render(self, ax, scaling):
        self.mobject.scale(scaling / 2)
        self.mobject.move_to(ax.c2p(self.start.x, self.start.y))
        self.mobject.shift(UP * scaling / 2 * (self.height / 2), RIGHT * scaling / 2 * (self.width / 2))
        return self


class Tiling:
    def __init__(self):
        self.mobject = Rectangle(WHITE, 0, 0)

    def union(self, rect):
        self.mobject = Union(self.mobject, rect)
