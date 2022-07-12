from LatexMobjects.Construction import tex_greedy, tex_tile, tex_greedy_explaination, tex_tiling_explaination
from LatexMobjects.Introduction import IntroTex
from Packing import Packing
from ParTypes import *

scaling = 5

def scan_line_y_cut(point):
    return point.y + point.x


def align_ax_origins(to_ax, from_ax):
    target = to_ax.c2p(0, 0)
    start = from_ax.c2p(0, 0)
    return target - start


def init_axes(scaling, offset=ORIGIN):
    ax = Axes(
        x_range=[0, 2, 1],
        y_range=[0, 2, 1],
        x_length=scaling,
        y_length=scaling,
        axis_config={
            "numbers_to_include": [1],
        }
    ).shift(LEFT * 3 + offset)

    invis_ax_size = 4
    invis_ax = Axes(
        x_range=[-invis_ax_size, invis_ax_size, 1],
        y_range=[-invis_ax_size, invis_ax_size, 1],
        x_length=invis_ax_size * scaling,
        y_length=invis_ax_size * scaling
    )
    invis_ax.shift(align_ax_origins(ax, invis_ax))
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
    def construct(self):
        animator = TilePackingAnimator()
        old_ax, packing = animator.animate(packing_type='BETA')
        beta_tile = packing.tiling_possible_points_polygons[9]
        ax, invis_ax = init_axes(scaling/10, old_ax.c2p(*beta_tile.point.to_vec2d()) + 3 * RIGHT)
        self.add(ax)
        self.add(old_ax)
        self.add(packing.base_rect.mobject)
        self.add(beta_tile.mobject)

