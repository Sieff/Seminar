from LatexMobjects.Construction import tex_greedy, tex_tile, tex_greedy_explaination, tex_tiling_explaination
from LatexMobjects.Introduction import IntroTex
from Packing import Packing
from ParTypes import *

scaling = 5

def scan_line_y_cut(point):
    return point.y + point.x


def align_ax_to_point(ax, point):
    start = ax.c2p(0, 0)
    return point - start


def init_axes(scaling, offset=ORIGIN, labels=True):
    if labels:
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling,
            axis_config={
                "numbers_to_include": [1],
            }
        ).shift(LEFT * 3 + offset)
    else:
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling
        ).shift(LEFT * 3 + offset)

    invis_ax_size = 4
    invis_ax = Axes(
        x_range=[-invis_ax_size, invis_ax_size, 1],
        y_range=[-invis_ax_size, invis_ax_size, 1],
        x_length=invis_ax_size * scaling,
        y_length=invis_ax_size * scaling
    )
    invis_ax.shift(align_ax_to_point(invis_ax, ax.c2p(0, 0)))
    return ax, invis_ax


class MyScene(Scene):
    def timed_que(self, duration=0):
        position = [6.5, -3, 0]
        radius = 0.03
        spacing = radius * 3
        dot1 = Dot(position, radius=radius)
        dot2 = Dot(position, radius=radius).shift(DOWN * spacing)
        dot3 = Dot(position, radius=radius).shift(DOWN * spacing * 2)
        self.wait(duration)
        self.play(AnimationGroup(Create(dot1),
                                 Create(dot2),
                                 Create(dot3)))
        self.play(LaggedStart(FadeOut(dot1),
                              FadeOut(dot2),
                              FadeOut(dot3), lag_ratio=1))


class Animator:
    def __init__(self):
        super().__init__()
        self.animations = []

    def play(self, animation):
        self.animations.append(animation)


class Introduction(MyScene):
    def construct(self):
        ax, invis_ax = init_axes(scaling)
        self.add(ax)
        packing = Packing(BaseRectangle(1, 1, 'INTRO', num_points=10), ax, scaling)
        self.play(AnimationGroup(FadeIn(packing.base_rect.mobject),
                                 FadeIn(packing.base_rect.label),
                                 IntroTex.mobject_writes[0]))
        self.play(AnimationGroup(FadeOut(packing.base_rect.label),
                                 LaggedStart(*packing.get_points_creations()),
                                 IntroTex.mobject_writes[1]))
        self.play(AnimationGroup(*packing.get_greedy_rectangle_transforms(),
                                 IntroTex.mobject_writes[2]))


class DiagonalPacking(MyScene):
    def construct(self):
        ax, invis_ax = init_axes(scaling)
        self.add(ax)
        packing = Packing(BaseRectangle(1, 1, 'DIAGONAL', num_points=10), ax, scaling)
        self.add(packing.base_rect.mobject)
        self.play(LaggedStart(*packing.get_points_creations()))
        self.play(LaggedStart(*packing.get_greedy_rectangle_transforms()))


class SweepingLine(MyScene):
    def construct(self):
        ax, invis_ax = init_axes(scaling)
        self.add(ax)
        packing = Packing(BaseRectangle(1, 1, 'INTRO', num_points=10), ax, scaling)
        self.add(packing.base_rect.mobject)
        self.play(LaggedStart(*packing.get_points_creations()))
        scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(1, 1)), color=ORANGE)
        self.play(FadeIn(scan_line))
        for point in packing.ordered_points:
            new_scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(point), color=ORANGE)
            self.play(Transform(scan_line, new_scan_line))
        self.play(FadeOut(scan_line))


class GreedyPackingAnimator(Animator):
    def animate(self, offset=ORIGIN, packing_type='GREEDYBETTER'):
        ax, invis_ax = init_axes(scaling, offset)
        packing = Packing(BaseRectangle(1, 1, packing_type, num_points=10), ax, scaling)
        self.play(LaggedStart(*packing.get_points_creations()))

        scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(1, 1)), color=ORANGE)
        self.play(FadeIn(scan_line))
        for idx, packed_rectangle in enumerate(packing.greedy_rectangles):
            point = packing.ordered_points[idx]
            new_scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(point), color=ORANGE)
            if idx > 0:
                self.play(AnimationGroup(FadeOut(packing.greedy_possible_points_polygons[idx - 1].mobject),
                                         LaggedStart(Transform(scan_line, new_scan_line),
                                                     FadeIn(packing.greedy_possible_points_polygons[idx].mobject),
                                                     lag_ratio=0.3)))
            else:
                self.play(LaggedStart(Transform(scan_line, new_scan_line),
                                      FadeIn(packing.greedy_possible_points_polygons[idx].mobject),
                                      lag_ratio=0.3))

            self.play(packing.get_greedy_rectangle_transforms()[idx])
            if idx == len(packing.greedy_rectangles) - 1:
                self.play(FadeOut(packing.greedy_possible_points_polygons[idx].mobject))
        self.play(FadeOut(scan_line))
        self.play(FadeIn(packing.greedy_unpacked_space))
        self.play(FadeOut(packing.greedy_unpacked_space))
        self.play(FadeIn(packing.greedy_unpacked_space))
        return ax, packing.base_rect.mobject


class GreedyPacking(Scene):
    def construct(self):
        animator = GreedyPackingAnimator()
        ax, base_rect = animator.animate()
        self.add(ax)
        self.add(base_rect)
        self.add(*tex_greedy_explaination.mobjects)
        for a in animator.animations:
            self.play(a)


class TilePackingAnimator(Animator):
    def animate(self, offset=ORIGIN, packing_type='GREEDYBETTER'):
        ax, invis_ax = init_axes(scaling, offset)
        packing = Packing(BaseRectangle(1, 1, packing_type, num_points=10), ax, scaling)
        self.play(LaggedStart(*packing.get_points_creations()))

        scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(1, 1)), color=ORANGE)
        self.play(FadeIn(scan_line))
        for idx, packed_rectangle in enumerate(packing.tiling_rectangles):
            point = packing.ordered_points[idx]
            new_scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(point), color=ORANGE)
            if idx > 0:
                self.play(AnimationGroup(FadeOut(packing.tiling_possible_points_polygons[idx - 1].mobject),
                                         LaggedStart(Transform(scan_line, new_scan_line),
                                                     FadeIn(packing.tiling_possible_points_polygons[idx].mobject),
                                                     lag_ratio=0.3)))
            else:
                self.play(LaggedStart(Transform(scan_line, new_scan_line),
                                      FadeIn(packing.tiling_possible_points_polygons[idx].mobject),
                                      lag_ratio=0.3))

            self.play(packing.get_tiling_rectangle_transforms()[idx])
            if idx == len(packing.tiling_rectangles) - 1:
                self.play(FadeOut(packing.tiling_possible_points_polygons[idx].mobject))

        self.play(FadeOut(scan_line))
        self.play(FadeIn(packing.tiling_unpacked_space))
        self.play(FadeOut(packing.tiling_unpacked_space))
        self.play(FadeIn(packing.tiling_unpacked_space))
        return ax, packing


class TilePacking(Scene):
    def construct(self):
        animator = TilePackingAnimator()
        ax, packing = animator.animate()
        self.add(ax)
        self.add(packing.base_rect.mobject)
        self.add(*tex_tiling_explaination.mobjects)
        for a in animator.animations:
            self.play(a)


class MultiPacking(Scene):
    def construct(self):
        greedy_animator = GreedyPackingAnimator()
        greedy_ax, greedy_base_rect = greedy_animator.animate(packing_type='GREEDYBETTER')
        tile_animator = TilePackingAnimator()
        tile_ax, packing = tile_animator.animate(offset=RIGHT * 6, packing_type='GREEDYBETTER')
        self.add(greedy_ax, greedy_base_rect, tile_ax, packing.base_rect.mobject)
        self.play(AnimationGroup(Write(tex_greedy.next_to(greedy_ax, UP)), Write(tex_tile.next_to(tile_ax, UP))))
        animation_pairs = zip(greedy_animator.animations, tile_animator.animations)
        for pair in animation_pairs:
            self.play(AnimationGroup(*pair))


class BetaProperties(Scene):
    def plot(self, ax, threshold):
        return ax.plot(lambda x: threshold / x, color=ORANGE, x_range=[threshold - 0.05, threshold / (threshold - 0.05), 0.01])

    def construct(self):
        animator = TilePackingAnimator()
        old_ax, packing = animator.animate(packing_type='BETA')
        beta_tile = packing.tiling_possible_points_polygons[9]
        beta_tile.mobject.set_color(WHITE).set_stroke(width=2)
        self.add(old_ax)
        self.add(packing.base_rect.mobject)
        self.play(FadeIn(beta_tile.mobject))

        ax, invis_ax = init_axes(scaling, labels=False)
        dashed_lines = VGroup(DashedLine(ax.c2p(0, 1), ax.c2p(1, 1)), DashedLine(ax.c2p(1, 0), ax.c2p(1, 1)))
        new_beta_tile = beta_tile.mobject.animate.scale(10).align_to(ax.c2p(0), LEFT + DOWN)
        self.play(new_beta_tile,
                  Transform(old_ax, ax),
                  FadeOut(packing.base_rect.mobject),
                  FadeIn(dashed_lines))

        brace_d = Brace(beta_tile.mobject, direction=DOWN)
        brace_d_label = Tex('$a_i$').next_to(brace_d, DOWN)
        brace_l = Brace(beta_tile.mobject, direction=LEFT)
        brace_l_label = Tex('$b_i$').next_to(brace_l, LEFT)
        self.play(FadeIn(brace_l, brace_d, brace_d_label, brace_l_label))

        x_label = Tex(r'$w = |a_i|$')
        y_label = Tex(r'$h = |b_i|$')
        ax.x_axis.add_labels({1: x_label})
        ax.y_axis.add_labels({1: y_label})
        self.play(LaggedStart(FadeOut(brace_l, brace_d, brace_d_label, brace_l_label),
                              FadeIn(x_label, y_label), lag_ratio=0.2))
        self.play(x_label.animate.become(Tex(r'$w$').move_to(x_label)),
                  y_label.animate.become(Tex(r'$h$').move_to(y_label)))

        threshold = 0.2
        graph = self.plot(ax, threshold)
        graph_label = Tex('f(x) = u / x', font_size=28).next_to(graph, UL)
        graph_label.shift(RIGHT * graph_label.width)
        graph_label.save_state()
        graph.save_state()
        new_graph = self.plot(ax, 0.8)
        new_label = Tex('f(x) = u / x', font_size=28).next_to(new_graph, UL).shift(RIGHT * graph_label.width)
        self.play(Create(graph))
        self.play(FadeIn(graph_label))
        self.play(Transform(graph, new_graph), Transform(graph_label, new_label))
        self.wait()
        self.play(Restore(graph), Restore(graph_label))

        h_line = Line(ax.c2p(0.2, -.05), ax.c2p(0.2, 1), stroke_width=2)
        x_label_2 = Tex(r'$u / h$')
        ax.x_axis.add_labels({0.2: x_label_2})
        self.play(FadeIn(h_line, x_label_2))

        rect = PackedRectangle(MyPoint(0, 0), MyPoint(0.2, 1)).render(ax, scaling)
        rect.mobject.stroke_width = 2
        rect.mobject.set_opacity(0.8)
        area = ax.get_area(graph, (0.2, 1), color=GREEN, stroke_width=2, opacity=0.8)
        self.play(FadeIn(rect.mobject, area))
