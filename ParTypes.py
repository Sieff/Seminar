from manim import *

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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return round(self.x * 1000000 + self.y * 1000)


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
        self.mobject = Dot(radius=0)

    def union(self, rect):
        self.mobject = Union(self.mobject, rect)
