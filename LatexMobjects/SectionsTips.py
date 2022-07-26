from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_red_area = Tex(r'$< \frac{1}{\beta} \text{area}(t_i)$', font_size=font_size)
tex_blue_area = Tex(r'$\geq \frac{1}{\beta} \text{area}(t_i)$', font_size=font_size)
tex_a_prime_smaller = Tex(r'$|a_i^\prime| \leq |a_i| - |a_i^\prime|$', font_size=font_size)
tex_a_statement = Tex(r'$2|a_i^\prime| \leq |a_i|$', font_size=font_size)

tex_sections_tips_proof = MyLatex([tex_red_area, tex_blue_area, tex_a_prime_smaller, tex_a_statement])

tex_gt_area = Tex(r'$\geq \frac{1}{\beta} \text{area}(t_i)$', font_size=font_size)
tex_lt_area = Tex(r'$< \frac{2}{\beta} \text{area}(t_i)$', font_size=font_size)

tex_sections_tips_info = MyLatex([tex_gt_area, tex_lt_area])
