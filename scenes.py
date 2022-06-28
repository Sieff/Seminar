from manim import *
import numpy as np
from ParTypes import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, RIGHT, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen


class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        square = Square()  # create a square

        self.play(Create(square))  # show the square on screen
        self.play(square.animate.rotate(PI / 4))  # rotate the square
        self.play(
            ReplacementTransform(square, circle)
        )  # transform the square into a circle
        self.play(
            circle.animate.set_fill(PINK, 0.5)
        )  # color the circle on screen


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            Rotate(left_square, angle=PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()


class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class CountingScene(Scene):
    def construct(self):
        # Create Decimal Number and add it to scene
        number = DecimalNumber().set_color(WHITE).scale(5)
        # Add an updater to keep the DecimalNumber centered as its value changes
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)

        self.wait()

        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 100), run_time=4, rate_func=linear)

        self.wait()


def order_points(points):
    point_array = []
    for point in points:
        point_array.append(point)
    point_array.sort(reverse=True, key=lambda p: p.x + p.y)
    return point_array


def get_vertices(start, polygon_points):
    start_index = 0
    for i in range(len(polygon_points)):
        if start == MyPoint(polygon_points[i][0], polygon_points[i][1]):
            start_index = i
            break
    polygon_points = np.roll(polygon_points, -start_index)
    first_point, polygon_points = polygon_points[0], polygon_points[1:]
    last_point = MyPoint(first_point[0], first_point[1])
    vertices = [last_point]
    for point in polygon_points:
        if last_point != MyPoint(point[0], point[1]):
            last_point = MyPoint(point[0], point[1])
        else:
            vertices.append(MyPoint(point[0], point[1]))
            last_point = MyPoint(point[0], point[1])
    return vertices


def get_maximal_rect_target(start, tile_points):
    vertices = get_vertices(start, tile_points)
    max_area = 0
    argmax_area = -1
    for i in range(len(vertices)):
        point = vertices[i]
        area = (point.x - start.x) * (point.y - start.y)
        if area > max_area:
            max_area = area
            argmax_area = i
    return vertices[argmax_area]


class GrowingRectangle(Scene):
    def construct(self):
        scaling = 5
        base_rect = BaseRectangle(1, 1)
        base_rect.add_point(0.55, 0.55)
        base_rect.add_point(0.8, 0.7)
        base_rect.add_point(0.9, 0.1)
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling,
        )
        self.add(ax)
        base_rect.render(ax, scaling / 2)
        self.add(base_rect.mobject)
        for point in base_rect.pointsSet:
            point.render(ax)
            self.add(point.mobject)
        self.wait()
        ordered_points = order_points(base_rect.pointsSet)
        tiling = Tiling()
        for point in ordered_points:
            packed_rectangle = PackedRectangle(point, MyPoint(1, 1))
            packed_rectangle.render(ax, scaling)
            tile = Difference(packed_rectangle.mobject, tiling.mobject)
            tile_points = ax.p2c(tile.points)
            maximal_rect_target = get_maximal_rect_target(packed_rectangle.start, tile_points)
            packed_rectangle = PackedRectangle(point, maximal_rect_target).render(ax, scaling)
            self.play(Transform(point.mobject, packed_rectangle.mobject))
            tiling.union(packed_rectangle.mobject)

            self.wait()