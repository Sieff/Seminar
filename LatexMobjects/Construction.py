from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_greedy = Tex('GreedyPacking', font_size=font_size)
tex_tile = Tex('TilePacking', font_size=font_size)

tex_greedy_explain = Tex(r'\begin{flushleft}'
                         r'GreedyPacking: For $i = 1, 2, \text{...}, n$,\\'
                         r'choose an axis-aligned rectangle $r_i \subseteq[0, 1]^2$\\'
                         r'of maximum area such that the lower left\\'
                         r' corner of $r_i$ is $s_i$, and $r_i$ is\\'
                         r'interior-disjoint from any $r_j, j<i$.'
                         r'\end{flushleft}', font_size=font_size)
tex_greedy_explaination = MyLatex([tex_greedy_explain])

tex_tiling_explain = Tex('\\begin{flushleft} TilePacking: Compute the tiling\\\\'
                         '$U = \\bigcup_{i=1}^n t_i$.\\\\'
                         'For $i = 1, \\text{...}, n$, independently,\\\\'
                         'choose an axis-aligned rectangle\\\\'
                         '$r_i \\subseteq t_i$ of maximum area.'
                         '\\end{flushleft}', font_size=font_size)
tex_tiling_explaination = MyLatex([tex_tiling_explain])
