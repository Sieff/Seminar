from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_unit_square = Tex('$U = [0,1]^2$', font_size=font_size)
tex_points_set = Tex('Finite points set $S, (0,0) \\in S$', font_size=font_size)
tex_rectangles = Tex('Axis aligned rectangles $\\forall s \\in S: r(s) \\subseteq U$', font_size=font_size).align_to(tex_points_set, LEFT).shift(DOWN)

IntroTex = MyLatex([tex_unit_square, tex_points_set, tex_rectangles])
