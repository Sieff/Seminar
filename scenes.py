from manim import *
from Packing import Packing
from ParTypes import *


def scan_line_y_cut(point):
    return point.y + point.x


def align_ax_origins(to_ax, from_ax):
    target = to_ax.c2p(0, 0)
    start = from_ax.c2p(0, 0)
    return target - start


class PackingGreedyRectangles(Scene):
    def construct(self):
        scaling = 5
        ax, invis_ax = self.init_axes(scaling)
        packing = Packing(BaseRectangle(1, 1, 'RANDOM', num_points=10), ax, scaling)
        self.add(packing.base_rect.mobject)
        self.play(LaggedStart(*packing.get_points_creations()))
        self.greedy(packing, invis_ax)

    def greedy(self, packing, invis_ax):
        scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(1, 1)), color=ORANGE)
        self.play(FadeIn(scan_line))
        for idx, packed_rectangle in enumerate(packing.greedy_rectangles):
            point = packing.ordered_points[idx]
            new_scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(point), color=ORANGE)
            self.play(Transform(scan_line, new_scan_line))
            self.play(FadeIn(packing.greedy_possible_points_polygons[idx].mobject))
            self.play(Transform(point.mobject, packed_rectangle.mobject))
            self.play(FadeOut(packing.greedy_possible_points_polygons[idx].mobject))
        self.play(FadeOut(scan_line))
        self.play(FadeIn(packing.greedy_unpacked_space))
        self.play(FadeOut(packing.greedy_unpacked_space))
        self.play(FadeIn(packing.greedy_unpacked_space))
        self.play(FadeOut(packing.greedy_unpacked_space))

    def tiling(self, packing, invis_ax):
        scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(1, 1)), color=ORANGE)
        self.play(FadeIn(scan_line))
        for idx, packed_rectangle in enumerate(packing.tiling_rectangles):
            point = packing.ordered_points[idx]
            new_scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(point), color=ORANGE)
            self.play(Transform(scan_line, new_scan_line))
            self.play(FadeIn(packing.tiling_possible_points_polygons[idx].mobject))
            self.play(Transform(point.mobject, packed_rectangle.mobject))
            self.play(FadeOut(packing.tiling_possible_points_polygons[idx].mobject))
        self.play(FadeOut(scan_line))
        self.play(FadeIn(packing.tiling_unpacked_space))
        self.play(FadeOut(packing.tiling_unpacked_space))
        self.play(FadeIn(packing.tiling_unpacked_space))
        self.play(FadeOut(packing.tiling_unpacked_space))

    def init_axes(self, scaling):
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling,
            axis_config={
                "numbers_to_include": [1],
            }
        ).shift(LEFT * 3)
        self.add(ax)

        invis_ax_size = 4
        invis_ax = Axes(
            x_range=[-invis_ax_size, invis_ax_size, 1],
            y_range=[-invis_ax_size, invis_ax_size, 1],
            x_length=invis_ax_size * scaling,
            y_length=invis_ax_size * scaling
        )
        invis_ax.shift(align_ax_origins(ax, invis_ax))
        return ax, invis_ax
