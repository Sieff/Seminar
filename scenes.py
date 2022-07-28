from LatexMobjects.BetaProperties import tex_beta_property_proof
from LatexMobjects.Charging import tex_charging
from LatexMobjects.Construction import tex_greedy, tex_tile, tex_greedy_explaination, tex_tiling_explaination
from LatexMobjects.Introduction import IntroTex
from LatexMobjects.Overlapping import tex_overlapping
from LatexMobjects.SectionsTips import tex_sections_tips_proof, tex_sections_tips_info
from LatexMobjects.Stripes import tex_stripes
from LatexMobjects.Trapezoids import tex_trapezoids
from LatexMobjects.Triangles import tex_triangles
from Packing import Packing
from ParTypes import *

MyRed = '#f21707'

scaling = 5


def scan_line_y_cut(point, slope=-1):
    return point.y + -1 * slope * point.x


def align_ax_to_point(ax, point):
    start = ax.c2p(0, 0)
    return point - start


def init_axes(scaling, offset=ORIGIN, labels=True, tips=True):
    if labels and tips:
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling,
            axis_config={
                "numbers_to_include": [1],
            }
        ).shift(LEFT * 3 + offset)
    elif not labels and tips:
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling
        ).shift(LEFT * 3 + offset)
    elif labels and not tips:
        ax = Axes(
            x_range=[0, 1, 1],
            y_range=[0, 1, 1],
            x_length=scaling,
            y_length=scaling,
            tips=False,
            axis_config={
                "numbers_to_include": [1],
            }
        ).shift(LEFT * 3 + offset)
    else:
        ax = Axes(
            x_range=[0, 1, 1],
            y_range=[0, 1, 1],
            tips=False,
            x_length=scaling,
            y_length=scaling
        ).shift(LEFT * 3 + offset)

    invis_ax_size = 4
    if not tips:
        local_scaling = scaling * 2
    else:
        local_scaling = scaling
    invis_ax = Axes(
        x_range=[-invis_ax_size, invis_ax_size, 1],
        y_range=[-invis_ax_size, invis_ax_size, 1],
        x_length=invis_ax_size * local_scaling,
        y_length=invis_ax_size * local_scaling,
        axis_config={
            "numbers_to_include": [1],
        }
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
        self.next_section()
        self.play(AnimationGroup(FadeOut(packing.base_rect.label),
                                 LaggedStart(*packing.get_points_creations()),
                                 IntroTex.mobject_writes[1]))
        self.next_section()
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
        return ax, packing.base_rect.mobject


class GreedyPacking(Scene):
    def construct(self):
        animator = GreedyPackingAnimator()
        ax, base_rect = animator.animate()
        self.add(ax)
        self.add(base_rect)
        self.add(*tex_greedy_explaination.mobjects)
        self.wait()
        for a in animator.animations:
            self.next_section()
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
        return ax, packing


class TilePacking(Scene):
    def construct(self):
        animator = TilePackingAnimator()
        ax, packing = animator.animate()
        self.add(ax)
        self.add(packing.base_rect.mobject)
        self.add(*tex_tiling_explaination.mobjects)
        self.wait()
        for a in animator.animations:
            self.next_section()
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
    def get_rectangle_corners(self, bottom_left, top_right):
        return [
            (top_right[0], top_right[1]),
            (bottom_left[0], top_right[1]),
            (bottom_left[0], bottom_left[0]),
            (top_right[0], bottom_left[0]),
        ]

    def plot(self, ax, u):
        return ax.plot(lambda x: u / x, color=ORANGE, x_range=[u / 2, 2.0, 0.01])

    def construct(self):
        animator = TilePackingAnimator()
        old_ax, packing = animator.animate(packing_type='BETA')
        beta_tile = packing.tiling_possible_points_polygons[9]
        beta_tile.mobject.set_color(WHITE).set_stroke(width=2)
        self.add(old_ax)
        self.add(packing.base_rect.mobject)
        self.play(FadeIn(beta_tile.mobject))
        self.next_section()

        ax, invis_ax = init_axes(scaling, labels=False)
        new_beta_tile = beta_tile.mobject.animate.scale(10).align_to(ax.c2p(0), LEFT + DOWN)
        self.play(new_beta_tile,
                  Transform(old_ax, ax),
                  FadeOut(packing.base_rect.mobject))
        self.next_section()

        brace_d = Brace(beta_tile.mobject, direction=DOWN)
        brace_d_label = Tex('$a_i$').next_to(brace_d, DOWN)
        brace_l = Brace(beta_tile.mobject, direction=LEFT)
        brace_l_label = Tex('$b_i$').next_to(brace_l, LEFT)
        self.play(FadeIn(brace_l, brace_d, brace_d_label, brace_l_label))
        self.next_section()

        x_label = Tex(r'$w = |a_i|$')
        y_label = Tex(r'$h = |b_i|$')
        ax.x_axis.add_labels({1: x_label})
        ax.y_axis.add_labels({1: y_label})
        dashed_lines = VGroup(DashedLine(ax.c2p(0, 1), ax.c2p(1, 1)), DashedLine(ax.c2p(1, 0), ax.c2p(1, 1)))
        self.play(LaggedStart(FadeOut(brace_l, brace_d, brace_d_label, brace_l_label),
                              AnimationGroup(FadeIn(x_label, y_label),
                                             FadeIn(dashed_lines)), lag_ratio=0.2))
        self.next_section()

        self.play(x_label.animate.become(Tex(r'$w$').move_to(x_label)),
                  y_label.animate.become(Tex(r'$h$').move_to(y_label)))
        self.next_section()

        self.play(tex_beta_property_proof.mobject_writes[0])
        self.next_section()

        u = 0.2
        graph = self.plot(ax, u)
        graph_label = Tex('f(x) = u / x', font_size=28).next_to(graph, UL)
        graph_label.shift(RIGHT * graph_label.width)
        graph_label.save_state()
        graph.save_state()
        # u = 1
        # new_graph = self.plot(ax, u)
        # new_label = Tex('f(x) = u / x', font_size=28).next_to(new_graph, UL).shift(RIGHT * graph_label.width)
        self.play(Create(graph))
        self.play(FadeIn(graph_label))
        # self.wait()
        # self.play(Transform(graph, new_graph), Transform(graph_label, new_label))
        # self.wait()
        # self.play(Restore(graph), Restore(graph_label))
        self.next_section()

        h_line = Line(ax.c2p(0.2, -.05), ax.c2p(0.2, 1), stroke_width=2)
        x_label_2 = Tex(r'$u / h$')
        ax.x_axis.add_labels({0.2: x_label_2})
        self.play(FadeIn(h_line, x_label_2))
        self.next_section()

        t = ValueTracker(0.2)

        def get_rectangle():
            polygon = Polygon(
                *[
                    ax.c2p(*i)
                    for i in self.get_rectangle_corners(
                        (0, 0), (t.get_value(), u / t.get_value())
                    )
                ]
            )
            polygon.set_fill(BLUE, opacity=0.5)
            return polygon

        polygon = always_redraw(get_rectangle)

        dot = Dot(radius=0.05)
        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), u / t.get_value())))
        dot.set_z_index(10)

        self.play(FadeIn(dot))
        self.play(FadeIn(polygon))
        self.play(FadeIn(Rectangle(width=0.2, height=0.2, color=BLUE, stroke_width=2, fill_opacity=0.8).next_to(tex_beta_property_proof.mobjects[1], LEFT)))
        self.play(tex_beta_property_proof.mobject_writes[1])
        self.next_section()
        self.play(t.animate.set_value(1), run_time=4)
        self.play(t.animate.set_value(0.2), run_time=4)
        self.next_section()

        rect = PackedRectangle(MyPoint(0, 0), MyPoint(0.2, 1)).render(ax, scaling)
        rect.mobject.stroke_width = 2
        rect.mobject.set_opacity(0.8)
        area = ax.get_area(graph, (0.2, 1), color=GREEN, stroke_width=2, opacity=0.8)
        self.play(FadeIn(area))

        for idx, write in enumerate(tex_beta_property_proof.mobject_writes):
            if idx <= 1:
                continue
            self.next_section()
            if idx == 2:
                self.play(FadeIn(Rectangle(width=0.2, height=0.2, color=GREEN, stroke_width=2, fill_opacity=0.8).next_to(tex_beta_property_proof.mobjects[idx], LEFT)))

            self.play(write)


class SectionsTips(Scene):
    def construct(self):
        animator = TilePackingAnimator()
        old_ax, packing = animator.animate(packing_type='BETA')
        ax, invis_ax = init_axes(scaling, labels=False)
        beta_tile = packing.tiling_possible_points_polygons[9]
        beta_tile.mobject.scale(10).align_to(ax.c2p(0), LEFT + DOWN)
        beta_tile.spread_vertices(10)
        beta_tile.mobject.set_color(WHITE).set_stroke(width=2)
        dashed_lines = VGroup(DashedLine(ax.c2p(0, 1), ax.c2p(1, 1)), DashedLine(ax.c2p(1, 0), ax.c2p(1, 1)))
        self.add(ax)
        self.add(beta_tile.mobject)
        self.add(dashed_lines)

        h_lines = []
        h_lines_create = []
        beta_tile.flip_vertices()
        for idx, v in enumerate(beta_tile.vertices[3: -1]):
            h_lines.append(Line(ax.c2p(0, v.y), ax.c2p(v.x, v.y), stroke_width=2))
            h_lines_create.append(Create(h_lines[idx]))
        self.play(LaggedStart(*h_lines_create))
        self.next_section()
        self.play(FadeOut(*h_lines))
        v_lines = []
        v_lines_create = []
        beta_tile.flip_vertices()
        for idx, v in enumerate(beta_tile.vertices[3: -1]):
            v_lines.append(Line(ax.c2p(v.x, 0), ax.c2p(v.x, v.y), stroke_width=2))
            v_lines_create.append(Create(v_lines[idx]))
        self.play(LaggedStart(*v_lines_create))
        self.next_section()

        right_tip = beta_tile.get_tip('r', ax, scaling)
        upper_tip = beta_tile.get_tip('u', ax, scaling)
        right_tip.mobject.set_color(BLUE)
        upper_tip.mobject.set_color(BLUE)
        main_body = Difference(Difference(beta_tile.mobject, right_tip.mobject), upper_tip.mobject)
        self.play(Create(right_tip.mobject))
        self.play(Create(upper_tip.mobject))

        r_label = Tex('right tip', font_size=28).next_to(right_tip.mobject, RIGHT)
        u_label = Tex('upper tip', font_size=28).next_to(upper_tip.mobject, UP).shift(RIGHT * 0.4)
        m_label = Tex(r'main body', font_size=28).next_to(main_body, RIGHT + UP, buff=-0.2)
        self.play(FadeIn(r_label, u_label, m_label))
        self.next_section()

        tiny_rect1 = Rectangle(width=0.2, height=0.2, color=BLUE, stroke_width=2, fill_opacity=0.8)
        tiny_rect2 = Rectangle(width=0.2, height=0.2, color=BLUE, stroke_width=2, fill_opacity=0.8)
        self.play(AnimationGroup(FadeIn(tiny_rect1.next_to(tex_sections_tips_info.mobjects[0], LEFT)),
                                 tex_sections_tips_info.mobject_writes[0],
                                 FadeIn(tiny_rect2.next_to(tex_sections_tips_info.mobjects[1], LEFT)),
                                 tex_sections_tips_info.mobject_writes[1]))
        self.next_section()

        m_prime = Tex(r'$t_i^\prime$', font_size=28).move_to(main_body).shift((DOWN + LEFT) * 0.1)
        a_brace = Brace(main_body, DOWN)
        b_brace = Brace(main_body, LEFT)
        a_prime = Tex(r'$a_i^\prime$', font_size=28).next_to(a_brace, DOWN)
        b_prime = Tex(r'$b_i^\prime$', font_size=28).next_to(b_brace, LEFT)
        self.play(LaggedStart(FadeOut(*v_lines),
                              FadeIn(a_brace, b_brace, a_prime, b_prime, m_prime), lag_ratio=0.3))
        self.next_section()

        self.remove(a_brace, b_brace, a_prime, b_prime, m_prime, upper_tip.mobject, right_tip.mobject, r_label,
                    u_label, m_label, *tex_sections_tips_info.mobjects, tiny_rect1, tiny_rect2)
        self.wait()
        self.next_section()

        if beta_tile.flipped:
            beta_tile.flip_vertices()
        rect = PackedRectangle(beta_tile.point, beta_tile.vertices[8]).render(ax, scaling)
        right_tip_bounding_rect = PackedRectangle(right_tip.point,
                                                  MyPoint(right_tip.vertices[1].x,
                                                          right_tip.vertices[-1].y)).render(ax, scaling)
        rect.mobject.set_color(RED)
        right_tip_bounding_rect.mobject.set_color(BLUE)
        self.play(FadeIn(right_tip.mobject))
        self.next_section()

        self.play(AnimationGroup(FadeIn(rect.mobject),
                                 ReplacementTransform(right_tip.mobject, right_tip_bounding_rect.mobject)))
        self.next_section()

        a_prime_abs = Tex(r'$|a_i^\prime|$', font_size=28).next_to(a_brace, DOWN)
        self.play(AnimationGroup(FadeIn(Rectangle(width=0.2, height=0.2, color=RED, stroke_width=2, fill_opacity=0.8)
                                        .next_to(tex_sections_tips_proof.mobjects[0], LEFT),
                                        a_prime_abs,
                                        a_brace),
                                 tex_sections_tips_proof.mobject_writes[0]))
        self.next_section()

        r_brace = Brace(right_tip_bounding_rect.mobject, DOWN)
        r_brace_label = Tex(r'$|a_i| - |a_i^\prime|$', font_size=28).next_to(r_brace, DOWN)
        self.play(AnimationGroup(FadeIn(Rectangle(width=0.2, height=0.2, color=BLUE, stroke_width=2, fill_opacity=0.8)
                                        .next_to(tex_sections_tips_proof.mobjects[1], LEFT),
                                        r_brace,
                                        r_brace_label),
                                 tex_sections_tips_proof.mobject_writes[1]))
        self.next_section()

        self.play(tex_sections_tips_proof.mobject_writes[2])
        self.next_section()

        self.play(tex_sections_tips_proof.mobject_writes[3])


class Triangles(Scene):
    def construct(self):
        animator = TilePackingAnimator()
        og_ax, packing = animator.animate(packing_type='WIDE')
        ax, invis_ax = init_axes(scaling, labels=False, tips=False)
        ax.shift(align_ax_to_point(ax, og_ax.c2p(0)))
        ax.shift(UP * 3)
        invis_ax.shift(align_ax_to_point(invis_ax, ax.c2p(0)))
        beta_tile = packing.tiling_possible_points_polygons[packing.base_rect.beta_tile_index]
        beta_tile.mobject.scale(10).align_to(ax.c2p(0), LEFT + DOWN)
        beta_tile.spread_vertices(5)
        beta_tile.mobject.set_color(WHITE).set_stroke(width=2)

        a_label = Tex('$a_i$', font_size=28).next_to(beta_tile.mobject, DOWN, buff=0.2)
        v_line = Line(ax.c2p(1, 2), ax.c2p(1, -5), stroke_width=2)
        triangle = beta_tile.triangle
        triangle.render(ax)
        t_label = Tex(r'$\Delta_i$', font_size=28).move_to((triangle.mobject.get_center() + triangle.mobject.get_corner(UR)) / 2)
        slope = invis_ax.plot(lambda x: -x, color=WHITE, stroke_width=2)
        self.add(beta_tile.mobject)
        self.play(FadeIn(a_label))
        self.next_section()

        self.play(FadeIn(slope))
        self.next_section()

        self.play(FadeIn(v_line))
        self.next_section()

        self.play(AnimationGroup(FadeOut(a_label), FadeIn(triangle.mobject, t_label)))
        self.next_section()

        self.remove(slope, v_line, t_label)
        triangle.mobject.set_fill(opacity=0)
        self.wait()
        self.next_section()

        point = MyPoint(0.4, -0.2)
        self.play(Create(point.render(ax).mobject))
        self.next_section()

        scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(1, 0.5)), color=ORANGE)
        self.play(FadeIn(scan_line))
        new_scan_line = invis_ax.plot(lambda x: -x + scan_line_y_cut(point), color=ORANGE)
        self.play(Transform(scan_line, new_scan_line))
        v_line_top = Intersection(beta_tile.mobject, PackedRectangle(MyPoint(point.x - 0.1, point.y), MyPoint(point.x + 0.3, 1)).render(ax, scaling).mobject)
        tile_v_line = Line(ax.c2p(*point.to_vec2d()), v_line_top.get_top(), color="#cc1400")
        tile_h_line = Line(ax.c2p(*point.to_vec2d()), ax.c2p(*MyPoint(1.25, -0.2).to_vec2d()), color="#cc1400")
        self.play(AnimationGroup(Create(tile_v_line, run_time=3),
                                 Create(tile_h_line, run_time=3)))
        self.next_section()

        self.play(FadeOut(tile_v_line, tile_h_line, scan_line, point.mobject))

        right_tip = beta_tile.get_tip('r', ax, scaling, beta=25).render(ax, 8)
        ai = MyLine(right_tip.vertices[0], MyPoint(0, 0)).render(ax)
        a_arrow = DoubleArrow(ai.mobject.get_left(), ai.mobject.get_right(), tip_length=0.1, stroke_width=2, buff=0).next_to(ai.mobject, UP, buff=0.2)
        a_prime = Tex(r'$|a_i^\prime|$', font_size=28).next_to(a_arrow, UP, buff=0.2)
        _lambda = 0.3
        trapezoid = triangle.get_trapezoid(_lambda, ai.length(), ax)
        self.play(FadeIn(right_tip.mobject, a_arrow, a_prime))
        self.next_section()

        tr_label = Tex(r'$A_i$', font_size=28).move_to(trapezoid.mobject.get_center())
        self.play(FadeIn(trapezoid.mobject, tr_label))
        self.next_section()

        l_d_arrow, l_d_label, l_d_l_divider, l_d_r_divider = trapezoid.get_l_d(ax)
        r_d_arrow, r_d_label, r_d_l_divider, r_d_r_divider = trapezoid.get_r_d(ax)
        r_arrow, r_label, r_divider = trapezoid.get_r(ax)
        self.play(FadeIn(r_arrow, r_label, r_divider))
        self.next_section()

        self.play(AnimationGroup(FadeIn(l_d_label, l_d_l_divider, l_d_arrow),
                                 FadeIn(r_d_arrow, r_d_label, r_d_r_divider, r_d_l_divider)))
        green_rect = PackedRectangle(trapezoid.vertices[0], trapezoid.vertices[3]).render(ax, scaling*2)
        green_rect.mobject.set_color(GREEN)
        blue_rect = PackedRectangle(trapezoid.vertices[1], trapezoid.vertices[3]).render(ax, scaling*2)
        for i, w in enumerate(tex_triangles.mobject_writes):
            self.next_section()
            if i == 0:
                self.play(FadeIn(Rectangle(width=0.2, height=0.2, color=GREEN, stroke_width=2, fill_opacity=0.8).next_to(tex_triangles.mobjects[i], LEFT),
                                 green_rect.mobject))
            if i == 1:
                self.play(FadeIn(Rectangle(width=0.2, height=0.2, color=BLUE, stroke_width=2, fill_opacity=0.8).next_to(tex_triangles.mobjects[i], LEFT),
                                 blue_rect.mobject))
            if i == 6:
                self.play(Write(Tex(r'(5)', font_size=32).next_to(tex_triangles.mobjects[i], LEFT)))
            self.play(w)


class Trapezoids(Scene):
    def construct(self):
        ax, invis_ax = init_axes(scaling)
        self.add(ax)
        packing = Packing(BaseRectangle(1, 1, 'INTRO', num_points=10), ax, scaling)
        self.add(packing.base_rect.mobject)
        _lambda = 0.3
        ai = MyLine(MyPoint(0, 0), MyPoint(1, 0)).render(ax)
        ai.mobject.set_color(RED)
        aip = ai.length() / 2
        trapezoid = Trapezoid(_lambda, aip).render(ax)
        pair = VGroup(ai.mobject, trapezoid.mobject)
        pair.scale(0.5)
        pair.align_to(ax.c2p(0.25, 0.5), UL)
        a_label = Tex(r'$a_i$', font_size=28).next_to(ai.mobject, UP, buff=0.1)
        A_label = Tex(r'$A_i$', font_size=28).next_to(trapezoid.mobject, DOWN, buff=0.1)
        self.play(FadeIn(pair, a_label, A_label))
        self.next_section()

        shape = MyPolygon(np.append(trapezoid.vertices[2:], [MyPoint(0, 0), MyPoint(0, 1), MyPoint(1, 1), MyPoint(1, 0)])).render(ax)
        shape.mobject.set_fill(opacity=0)
        self.play(FadeIn(shape.mobject))
        self.next_section()

        tex_corner1 = Tex(r'$(\frac{\lambda}{2}, -\frac{\lambda}{2})$', font_size=28).next_to(trapezoid.vertices[3].render(ax).mobject, DL, buff=0)
        tex_corner2 = Tex(r'$(\frac{1}{2}, -\frac{\lambda}{2})$', font_size=28).next_to(trapezoid.vertices[2].render(ax).mobject, DR, buff=0)
        self.play(FadeIn(tex_corner1, tex_corner2, trapezoid.vertices[3].mobject, trapezoid.vertices[2].mobject))
        self.next_section()

        self.play(LaggedStart(FadeOut(a_label, A_label),
                              pair.animate.align_to(ax.c2p(0.25, 1), UL)))
        self.next_section()

        self.play(pair.animate.align_to(ax.c2p(0.25, 0), UL))
        self.next_section()
        self.play(pair.animate.align_to(ax.c2p(0, 0), UL))
        self.next_section()
        self.play(pair.animate.scale(2).align_to(ax.c2p(0, 0), UL))
        self.next_section()
        self.play(pair.animate.scale(0.01).align_to(ax.c2p(1, 0), UR), run_time=4)
        self.next_section()
        self.play(pair.animate.scale(100).align_to(ax.c2p(0, 0), UL), run_time=4)
        below_area = MyPolygon(np.append(trapezoid.vertices[2:], [MyPoint(0, 0), MyPoint(1, 0)])).render(ax)
        u = MyPolygon([MyPoint(0, 0), MyPoint(0, 1), MyPoint(1, 1), MyPoint(1, 0)]).render(ax)
        below_area.mobject.set_color(ORANGE)
        u.mobject.set_color(GREEN)
        for i, w in enumerate(tex_trapezoids.mobject_writes):
            self.next_section()
            if i == 0:
                self.play(AnimationGroup(FadeIn(Rectangle(width=0.2, height=0.2, color=ORANGE, stroke_width=2, fill_opacity=0.8).next_to(tex_trapezoids.mobjects[i], LEFT),
                                                below_area.mobject),
                                         FadeOut(pair)))
            if i == 1:
                self.play(FadeIn(Rectangle(width=0.2, height=0.2, color=GREEN, stroke_width=2, fill_opacity=0.8).next_to(tex_trapezoids.mobjects[i], LEFT),
                                 u.mobject))
            if i == 2:
                shape.mobject.set_fill(opacity=0.5)
                self.play(AnimationGroup(FadeIn(Rectangle(width=0.2, height=0.2, color=BLUE, stroke_width=2, fill_opacity=0.8).next_to(tex_trapezoids.mobjects[i], LEFT),
                                                shape.mobject),
                                         FadeOut(u.mobject, below_area.mobject)))
            self.play(w)


class Overlapping(Scene):
    def construct(self):
        animator = TilePackingAnimator()
        og_ax, packing = animator.animate(packing_type='WIDE')
        ax, invis_ax = init_axes(scaling, labels=False, tips=False)
        ax.shift(align_ax_to_point(ax, og_ax.c2p(0)))
        ax.shift(UP * 3)
        invis_ax.shift(align_ax_to_point(invis_ax, ax.c2p(0)))
        beta_tile = packing.tiling_possible_points_polygons[packing.base_rect.beta_tile_index]
        beta_tile.mobject.scale(10).align_to(ax.c2p(0), LEFT + DOWN)
        beta_tile.spread_vertices(5)
        beta_tile.mobject.set_color(WHITE).set_stroke(width=2)

        triangle = beta_tile.triangle
        triangle.render(ax)
        triangle.mobject.set_fill(opacity=0)

        right_tip = beta_tile.get_tip('r', ax, scaling, beta=25).render(ax, 8)
        aj = MyLine(right_tip.vertices[0], MyPoint(0, 0)).render(ax)
        _lambda = 0.45
        j_trapezoid = triangle.get_trapezoid(_lambda, aj.length(), ax)
        j_trapezoid.mobject.set_fill(opacity=0)
        j_trapezoid.set_label('j')
        j_label = Tex(r'$a_j^\prime$', font_size=28, color=RED).align_to(j_trapezoid.mobject, UL).shift(DOWN * 0.1 + RIGHT * 0.4)
        l_j = MyLine(MyPoint(-2, 0), MyPoint(10, 0)).render(invis_ax)
        l_j_label = Tex(r'$l_j$', font_size=28).next_to(j_label, LEFT, buff=1)

        self.add(l_j.mobject, l_j_label, beta_tile.mobject, triangle.mobject, right_tip.mobject, j_trapezoid.mobject, j_label)
        self.wait()
        self.next_section()

        new_scaling = 0.65 * 0.5

        triangle = Triangle(new_scaling).render(ax)
        ai = MyLine(MyPoint(0, 0), MyPoint(new_scaling, 0)).render(ax)
        trapezoid = triangle.get_trapezoid(_lambda, ai.length()/2, ax)

        triangle.mobject.set_color(color=ORANGE).set_fill(opacity=0)
        ai.mobject.set_color(color=ORANGE)
        trapezoid.mobject.set_color(color=ORANGE).set_fill(opacity=0)

        i_t_height = _lambda * (ai.length() / 2)
        i_intersection = MyLine(MyPoint(_lambda * ai.length() / 4, -_lambda * ai.length() / 4), MyPoint(new_scaling, -_lambda * ai.length() / 4)).render(ax)
        i_intersection.mobject.set_color(MyRed)

        l_i = MyLine(MyPoint(-2, 0), MyPoint(10, 0)).render(invis_ax)
        l_i.mobject.align_to(ax.c2p(0, i_t_height * 0.5), UP)
        l_i_label = Tex(r'$l_i$', font_size=28).next_to(l_i.mobject, UP, buff=0.1).align_to(l_j_label, LEFT)
        l_i_group = VGroup(l_i.mobject, l_i_label)

        secondary = VGroup(ai.mobject, triangle.mobject, trapezoid.mobject, i_intersection.mobject).align_to(ax.c2p(0.12, i_t_height * 0.5), UL)
        i_label = Tex(r'$a_i$', color=ORANGE, font_size=28).next_to(secondary, UP, buff=0.1)
        group = VGroup(secondary, i_label)
        self.play(FadeIn(group))
        self.play(FadeIn(Line(ORIGIN, RIGHT * 0.2, color=MyRed).next_to(tex_overlapping.mobjects[0], LEFT)))
        self.play(tex_overlapping.mobject_writes[0])
        self.next_section()

        self.play(FadeIn(l_i_group))
        self.next_section()

        self.play(FadeOut(l_i_group))
        self.next_section()

        self.play(group.animate.shift(RIGHT * 0.8))
        dot = MyPoint(0.495, 0.015).render(ax)
        dot.mobject.set_color(MyRed)
        self.play(FadeIn(dot.mobject))
        self.play(FadeOut(dot.mobject))
        self.play(FadeIn(dot.mobject))
        self.next_section()
        self.play(FadeOut(dot.mobject))
        self.play(group.animate.shift(RIGHT * 1.2))
        self.next_section()

        group = VGroup(ai.mobject, triangle.mobject, trapezoid.mobject, i_label, i_intersection.mobject)

        self.play(group.animate.shift(LEFT * 2))
        self.play(tex_overlapping.mobject_writes[1])
        self.next_section()

        new_i_intersection = MyLine(MyPoint(_lambda * ai.length() / 2, -_lambda * ai.length() / 2), MyPoint(new_scaling, -_lambda * ai.length() / 2)).render(ax)
        new_i_intersection.mobject.set_color(MyRed).align_to(group, RIGHT).align_to(ax.c2p(0), UP)

        self.play(AnimationGroup(group.animate.shift(ax.c2p(0.12, i_t_height) - group[1].get_corner(UL)),
                                 ReplacementTransform(i_intersection.mobject, new_i_intersection.mobject)))

        for i, w in enumerate(tex_overlapping.mobject_writes):
            if i <= 1:
                continue
            self.next_section()
            if i == 3:
                self.add(MyLine(MyPoint(0, 0), MyPoint(-2, 0)).render(invis_ax).mobject)
                self.play(FadeOut(l_j.mobject))
            self.play(w)


class Charging(Scene):
    def construct(self):
        ax, invis_ax = init_axes(scaling, labels=False, tips=False)
        ax.shift(UP * 3).shift(RIGHT)
        invis_ax.shift(align_ax_to_point(invis_ax, ax.c2p(0)))
        _lambda = 0.3

        ajp_len = 0.8
        ajp = MyLine(MyPoint(ajp_len, 0), MyPoint(0, 0)).render(ax)
        j_trapezoid = Trapezoid(_lambda, ajp.length()).render(ax)
        j_trapezoid.mobject.set_fill(opacity=0)
        j_trapezoid.mobject.set_color(WHITE)
        j_trapezoid.set_label('j')

        self.add(j_trapezoid.mobject, j_trapezoid.label)
        self.wait()
        self.next_section()

        ai = MyLine(MyPoint(0, 0), MyPoint(2 * ajp_len / (2 - _lambda), 0)).render(ax)
        i_trapezoid = Trapezoid(_lambda, ai.length() / 2).render(ax)
        i_trapezoid.set_label('i', ORANGE)
        ai.mobject.set_color(color=ORANGE).shift(ax.c2p(0) - i_trapezoid.points[3])
        i_trapezoid.mobject.set_color(color=ORANGE).set_fill(opacity=0)
        i_trapezoid.shift(ax, ax.c2p(0) - i_trapezoid.points[3])
        i_group = VGroup(i_trapezoid.mobject, i_trapezoid.label, ai.mobject)

        self.play(FadeIn(i_group))
        self.next_section()

        u_arr, u_label, l_divider, r_divider = i_trapezoid.get_u(ax)
        u_label.shift(UP * 0.3, RIGHT * 0.1)
        u_group = VGroup(u_arr, u_label, l_divider, r_divider)
        l_arr, l_label, u_divider, d_divider = i_trapezoid.get_l(ax)
        l_group = VGroup(l_arr, l_label, u_divider, d_divider)

        self.play(AnimationGroup(FadeIn(u_group), tex_charging.mobject_writes[0]))
        self.next_section()
        self.play(AnimationGroup(FadeIn(l_group), tex_charging.mobject_writes[1]))
        self.next_section()

        triangle_tip = MyPoint(ajp_len * _lambda / (_lambda - 1), ajp_len * _lambda / (1 - _lambda))
        triangle = Triangle(
            custom_vertices=[triangle_tip, j_trapezoid.vertices[0], j_trapezoid.vertices[1]]).render(ax)
        triangle.mobject.align_to(j_trapezoid.points[1], DR)
        self.play(FadeIn(triangle.mobject))
        self.next_section()

        smaller_similar_triangle = Triangle(
            custom_vertices=[triangle_tip, i_trapezoid.vertices[0], i_trapezoid.vertices[1]]).render(ax)
        smaller_similar_triangle.mobject.align_to(i_trapezoid.points[1], DR)
        smaller_similar_triangle.mobject.set_color(RED)
        self.play(FadeIn(smaller_similar_triangle.mobject))
        self.next_section()

        self.play(FadeOut(smaller_similar_triangle.mobject))
        self.next_section()

        similar_triangle = Triangle(custom_vertices=[i_trapezoid.vertices[0], i_trapezoid.vertices[2], i_trapezoid.vertices[3]]).render(ax)
        similar_triangle.mobject.align_to(i_trapezoid.points[0], UL)
        similar_triangle.mobject.set_color(RED)

        r_d_arr, r_d_label, r_d_l_divider, r_d_r_divider = i_trapezoid.get_r_d(ax, label=r'$\frac{1 - \lambda}{2 - \lambda} |a_j^\prime|$')
        r_d_label.shift(RIGHT * 0.2)
        r_d_group = VGroup(r_d_arr, r_d_label, r_d_l_divider, r_d_r_divider)

        self.play(AnimationGroup(FadeIn(similar_triangle.mobject, r_d_group),
                                 FadeOut(i_trapezoid.label),
                                 triangle.mobject.animate.set_fill(opacity=0)))

        self.next_section()
        self.play(FadeOut(u_group))

        r_divider = Line(ax.c2p(*j_trapezoid.vertices[1].to_vec2d()), ax.c2p(*MyPoint(j_trapezoid.vertices[1].x, j_trapezoid.vertices[1].y - 0.05).to_vec2d()), stroke_width=1)
        aj_arr = DoubleArrow(start=ax.c2p(*j_trapezoid.vertices[0].as_coordinates()), end=ax.c2p(*j_trapezoid.vertices[1].as_coordinates()), tip_length=0.1, stroke_width=2, buff=0)
        aj_arr.next_to(j_trapezoid.points[1], DOWN, buff=0.03).align_to(r_divider, RIGHT)
        label = Tex(r'$|a_j^\prime|$', font_size=28).next_to(aj_arr, DOWN, buff=0.08).shift(RIGHT)
        aj_group = VGroup(aj_arr, label, r_divider)

        self.play(FadeIn(aj_group))
        self.next_section()

        d_divider = Line(ax.c2p(*j_trapezoid.vertices[0].to_vec2d()), ax.c2p(*MyPoint(triangle_tip.x - 0.05, j_trapezoid.vertices[0].y).to_vec2d()), stroke_width=1)
        u_divider = Line(ax.c2p(*triangle_tip.to_vec2d()), ax.c2p(*MyPoint(triangle_tip.x - 0.05, triangle_tip.y).to_vec2d()), stroke_width=1)
        h_arr = DoubleArrow(start=ax.c2p(*MyPoint(triangle_tip.x - 0.05, j_trapezoid.vertices[0].y).to_vec2d()),
                            end=ax.c2p(*MyPoint(triangle_tip.x - 0.05, triangle_tip.y).to_vec2d()),
                            tip_length=0.1, stroke_width=2, buff=0)
        h_arr.shift(RIGHT * 0.02)
        h_label = Tex(r'?', font_size=28).next_to(h_arr, LEFT, buff=0.08)
        h_group = VGroup(h_arr, h_label, d_divider, u_divider)
        self.play(FadeIn(h_group))
        self.next_section()

        self.play(tex_charging.mobject_writes[2])
        self.next_section()
        self.play(tex_charging.mobject_writes[3])
        self.next_section()

        new_triangle = triangle.mobject.copy().set_color(color=RED).set_fill(opacity=0.5)
        self.play(AnimationGroup(FadeOut(triangle.mobject),
                                 ReplacementTransform(similar_triangle.mobject, new_triangle)))

        tiny_rect = Rectangle(width=0.2, height=0.2, color=RED, stroke_width=2, fill_opacity=0.8).next_to(tex_charging.mobjects[4], LEFT).shift(RIGHT)
        tex_charging.mobjects[4].shift(RIGHT)
        eq_label = Tex(r'(7)', font_size=32).next_to(tiny_rect, LEFT)

        for i in range(4, 8):
            if i > 4:
                self.next_section()
            if i == 4:
                self.play(FadeIn(eq_label))
                self.play(FadeIn(tiny_rect))
            self.play(tex_charging.mobject_writes[i])


class Stripes(Scene):
    def construct(self):
        ax, invis_ax = init_axes(scaling, labels=False, tips=False)
        ax.shift(UP * 3)
        invis_ax.shift(align_ax_to_point(invis_ax, ax.c2p(0)))
        _lambda = 0.3

        ajp_len = 1
        ajp = MyLine(MyPoint(ajp_len, 0), MyPoint(0, 0)).render(ax)
        j_trapezoid = Trapezoid(_lambda, ajp.length()).render(ax)
        j_trapezoid.mobject.set_fill(opacity=0)
        j_trapezoid.mobject.set_color(WHITE)
        j_trapezoid.set_label('j')
        l_j = MyLine(MyPoint(-2, 0), MyPoint(10, 0)).render(invis_ax)
        l_j_label = Tex(r'$l_j$', font_size=28).next_to(j_trapezoid.mobject, LEFT).align_to(l_j.mobject, UP).shift(DOWN * 0.2)

        self.add(j_trapezoid.mobject, j_trapezoid.label, l_j_label, l_j.mobject)
        self.wait()
        self.next_section()

        i1_factor = 39/40
        ai1 = MyLine(MyPoint(0, 0), MyPoint(ajp_len * i1_factor, 0)).render(ax)
        i1_trapezoid = Trapezoid(_lambda, ai1.length() / 2).render(ax)
        i1_trapezoid.set_label('i_1', ORANGE)
        shift_amount = ax.c2p(0.1, -0.03) - i1_trapezoid.points[3]
        ai1.mobject.set_color(color=ORANGE).shift(shift_amount)
        i1_trapezoid.mobject.set_color(color=ORANGE).set_fill(opacity=0)
        i1_trapezoid.shift(ax, shift_amount)
        i1_group = VGroup(i1_trapezoid.mobject, i1_trapezoid.label, ai1.mobject)

        self.play(FadeIn(i1_group))
        self.next_section()

        i1_l_bound = invis_ax.plot(lambda x: -x + scan_line_y_cut(i1_trapezoid.vertices[0]), color=ORANGE)
        i1_r_bound = invis_ax.plot(lambda x: -x + scan_line_y_cut(i1_trapezoid.vertices[1]), color=ORANGE)
        i1_stripe_label = Tex(r'$\Xi_{i_1}$', font_size=28, color=ORANGE).next_to(i1_trapezoid.mobject, DR, buff=2).shift(DOWN * 0.3)
        i1_bounds = VGroup(i1_r_bound, i1_l_bound, i1_stripe_label)

        self.play(FadeIn(i1_bounds))
        self.next_section()

        ai2 = MyLine(MyPoint(0, 0), MyPoint(ajp_len * 7 / 16, 0)).render(ax)
        i2_trapezoid = Trapezoid(_lambda, ai2.length() / 2).render(ax)
        i2_trapezoid.set_label('i_2', BLUE)
        shift_amount = ax.c2p(0.55, -0.04) - i2_trapezoid.points[3]
        ai2.mobject.set_color(color=BLUE).shift(shift_amount)
        i2_trapezoid.mobject.set_color(color=BLUE).set_fill(opacity=0)
        i2_trapezoid.shift(ax, shift_amount)
        i2_group = VGroup(i2_trapezoid.mobject, i2_trapezoid.label, ai2.mobject)

        self.play(FadeIn(i2_group))

        i2_l_bound = invis_ax.plot(lambda x: -x + scan_line_y_cut(i2_trapezoid.vertices[0]), color=BLUE)
        i2_r_bound = invis_ax.plot(lambda x: -x + scan_line_y_cut(i2_trapezoid.vertices[1]), color=BLUE)
        i2_stripe_label = Tex(r'$\Xi_{i_2}$', font_size=28, color=BLUE).next_to(i2_trapezoid.mobject, DR, buff=2).shift(DOWN * 0.3)
        i2_bounds = VGroup(i2_r_bound, i2_l_bound, i2_stripe_label)

        self.play(FadeIn(i2_bounds))
        self.next_section()

        shift_amount = ax.c2p(*(i2_trapezoid.vertices[0] + MyPoint(-0.125, 0.125)).as_coordinates()) - i2_trapezoid.points[0]

        self.play(i2_group.animate.shift(shift_amount))
        self.next_section()
        self.play(i2_group.animate.shift(-shift_amount))
        self.next_section()

        forbidden_triangle = Triangle(custom_vertices=[i1_trapezoid.vertices[1], i1_trapezoid.vertices[2],
                                                       MyPoint(i1_trapezoid.vertices[2].x + _lambda * (ai1.length()/2), i1_trapezoid.vertices[2].y)])
        forbidden_triangle.render(ax)
        forbidden_triangle.mobject.set_color(MyRed).align_to(i1_trapezoid.points[1], UL)

        self.play(FadeIn(forbidden_triangle.mobject))
        self.next_section()
        self.play(forbidden_triangle.mobject.animate.align_to(i1_trapezoid.points[0], UL))
        self.next_section()
        arr, label, l_divider, r_divider = i1_trapezoid.get_l_d(ax, r'$\lambda |a_{i_1}^\prime|$')
        forbidden_triangle.mobject.z_index = 1
        l_divider.z_index = 0
        self.play(FadeIn(arr, label, l_divider, r_divider))
        self.next_section()
        self.play(FadeOut(arr, label, l_divider, r_divider))
        self.play(forbidden_triangle.mobject.animate.align_to(i1_trapezoid.points[1], UL))
        self.play(tex_stripes.mobject_writes[0])
        self.play(tex_stripes.mobject_writes[1])
        self.next_section()

        i1_triangle = Triangle(custom_vertices=[MyPoint(0, 0), MyPoint(i1_factor, 0), MyPoint(i1_factor, -i1_factor)]).render(ax)
        i1_triangle.mobject.align_to(i1_trapezoid.mobject, UL).set_color(ORANGE)
        i1_triangle_label = Tex(r'$\Delta_{i_1}$', font_size=28, color=ORANGE).next_to(i1_triangle.mobject, DR, buff=0).shift(UP * 1.5 + LEFT * 0.75)
        self.play(FadeIn(i1_triangle.mobject, i1_triangle_label))
        self.next_section()

        self.play(FadeOut(i1_triangle.mobject, i1_triangle_label, forbidden_triangle.mobject))

        i1_big_group = VGroup(ai1.mobject, i1_bounds)
        i2_big_group = VGroup(i2_group, i2_bounds)
        temporal_shift = DOWN * 0.5 + RIGHT * 0.3
        temporal_shift2 = RIGHT * 0.2 + UP * 0.15

        self.play(AnimationGroup(i2_big_group.animate.shift(temporal_shift2),
                                 i2_group.animate.shift(temporal_shift2),
                                 i1_big_group.animate.shift(temporal_shift),
                                 i1_group.animate.shift(temporal_shift)))
        self.next_section()
        shift_amount = ax.c2p(scan_line_y_cut(i1_trapezoid.vertices[0]), 0) - ax.c2p(*i1_trapezoid.vertices[3].as_coordinates()) + UP * 0.5 + LEFT * 0.5
        shift_amount2 = ax.c2p(scan_line_y_cut(i2_trapezoid.vertices[0]), 0) - ax.c2p(*i2_trapezoid.vertices[3].as_coordinates()) + DOWN * 0.15 + RIGHT * 0.15

        ai3 = MyLine(MyPoint(0, 0), MyPoint(ajp_len * 4 / 10, 0)).render(ax)
        i3_trapezoid = Trapezoid(_lambda, ai3.length() / 2).render(ax)
        i3_trapezoid.set_label('i_1', ORANGE)
        shift_amount3 = ax.c2p(0.1, -0.01) - i3_trapezoid.points[3]
        ai3.mobject.set_color(color=ORANGE).shift(shift_amount3)
        i3_trapezoid.mobject.set_color(color=ORANGE).set_fill(opacity=0)
        i3_trapezoid.shift(ax, shift_amount3)
        i3_group = VGroup(i3_trapezoid.mobject, ai3.mobject)

        self.play(FadeIn(i3_group))
        self.next_section()

        orange_group = VGroup(i1_group, i3_group)
        self.play(orange_group.animate.shift(shift_amount))
        self.play(i2_group.animate.shift(shift_amount2))
        self.next_section()

        shift_amount = ax.c2p(-0.027, 0.027) - ax.c2p(0)
        self.play(i3_group.animate.shift(shift_amount))
        self.next_section()

        self.play(FadeOut(i3_group, i1_bounds, i2_group, i2_bounds))
        self.next_section()

        last_triangle = Polygon(i1_trapezoid.mobject.get_corner(UR), ai1.mobject.get_corner(UR), i1_trapezoid.mobject.get_corner(DR),
                                color=ORANGE, fill_opacity=0.5)
        self.play(FadeIn(last_triangle))
        self.next_section()

        l_arr = DoubleArrow(start=i1_trapezoid.mobject.get_corner(UR), end=i1_trapezoid.mobject.get_corner(DR), tip_length=0.1, stroke_width=2, buff=0).next_to(last_triangle, LEFT, buff=0.08)
        l_label = Tex(r'$\lambda |a_{i_1}^\prime|$', font_size=28).next_to(l_arr, LEFT, buff=0.08)
        self.play(FadeIn(l_arr, l_label))
        self.next_section()

        u_arr = DoubleArrow(start=i1_trapezoid.mobject.get_corner(UR), end=ai1.mobject.get_corner(UR), tip_length=0.1, stroke_width=2, buff=0).next_to(last_triangle, UP, buff=0.08)
        u_label = Tex(r'$|a_{i_1}| - |a_{i_1}^\prime|$', font_size=28).next_to(u_arr, UP, buff=0.08)
        l_divider = Line(i1_trapezoid.mobject.get_corner(UR), i1_trapezoid.mobject.get_corner(UR) + UP * 0.2, stroke_width=1)
        r_divider = Line(ai1.mobject.get_corner(UR), ai1.mobject.get_corner(UR) + UP * 0.2, stroke_width=1)
        self.play(FadeIn(u_arr, u_label, l_divider, r_divider))
        self.next_section()

        self.play(tex_stripes.mobject_writes[2])
        self.next_section()

        self.play(FadeOut(l_arr, l_label, u_arr, u_label, l_divider, r_divider))

        self.play(Rotate(last_triangle, axis=RIGHT))
        self.next_section()

        last_group = VGroup(i1_group, last_triangle)
        last_line = MyLine(MyPoint(ajp_len, 0), MyPoint(ajp_len, 2)).render(ax)

        self.play(FadeIn(last_line.mobject))
        self.next_section()

        self.play(last_group.animate.align_to(last_line.mobject, RIGHT))
        self.next_section()

        lambda_bound = invis_ax.plot(lambda x: -x * _lambda + scan_line_y_cut(j_trapezoid.vertices[1], slope=-_lambda), color=BLUE)
        diagonal_bound = invis_ax.plot(lambda x: -x + scan_line_y_cut(MyPoint(0, 0)), color=BLUE)

        self.play(FadeIn(lambda_bound, diagonal_bound))
