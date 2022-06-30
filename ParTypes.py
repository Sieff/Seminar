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

    def to_vec(self):
        return np.array([self.x, self.y])

    def __eq__(self, other):
        return Decimal(f"{self.x:.9f}") == Decimal(f"{other.x:.9f}") and \
               Decimal(f"{self.y:.9f}") == Decimal(f"{other.y:.9f}")

    def __hash__(self):
        return round(self.x * 1000000 + self.y * 1000)

    def __str__(self):
        return 'X: ' + str(self.x) + ', Y: ' + str(self.y)

    def __repr__(self):
        return '<MyPoint: ' + self.__str__() + '>'


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
