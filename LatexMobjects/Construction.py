from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_greedy = Tex('GreedyPacking', font_size=font_size)
tex_tile = Tex('TilePacking', font_size=font_size)

tex_greedy_explain = Tex('GreedyPacking: For $i = 1, 2, \\text{...}, n$, choose an axis-aligned ' +
                         'rectangle $r_i \\subseteq[0, 1]^2$ of maximum area such that the lower left corner of ' +
                         '$r_i$ is $s_i$, and $r_i$ is interior-disjoint from any $r_j, j<i$.')
