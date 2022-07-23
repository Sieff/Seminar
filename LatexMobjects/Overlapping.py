from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_red_section = Tex(r'$= l_j \cap \Delta_i$', font_size=font_size)
tex_first_claim = Tex(r'$l_j \cap \Delta_i \subseteq a_j^\prime$', font_size=font_size)
tex_red_section_value = Tex(r'$|l_j \cap \Delta_i| \geq (1 - \lambda) * |a_i^\prime| + |a_i^\prime|$', font_size=font_size)
tex_equation1 = Tex(r'$|a_j^\prime| \geq |l_j \cap \Delta_i|$', font_size=font_size)
tex_equation2 = Tex(r'$\geq (1 - \lambda) * |a_i^\prime| + |a_i^\prime|$', font_size=font_size)
tex_equation3 = Tex(r'$= (2 - \lambda) * |a_i^\prime|$', font_size=font_size)

tex_overlapping = MyLatex([tex_red_section, tex_first_claim, tex_red_section_value, tex_equation1, tex_equation2, tex_equation3])
