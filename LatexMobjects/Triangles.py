from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_green_area = Tex(r'$= \frac{\lambda|a_i^\prime| * \lambda|a_i^\prime|}{2} = \frac{\lambda^2}{2} * |a_i^\prime|^2$', font_size=font_size)
tex_blue_area = Tex(r'$= \lambda|a_i^\prime| * (1 - \lambda)|a_i^\prime| = \lambda(1-\lambda) * |a_i^\prime|^2$', font_size=font_size)
tex_area_start = Tex(r'$\text{area}(A_i) = \frac{\lambda^2}{2} * |a_i^\prime|^2 + \lambda(1-\lambda) * |a_i^\prime|^2$', font_size=font_size)
tex_area_middle = Tex(r'$= \frac{\lambda(2 - \lambda)}{2} * |a_i^\prime|^2$', font_size=font_size)
tex_area_end = Tex(r'$\overset{(4)}{>} \frac{\lambda(2 - \lambda) * e^{\beta - 5}}{2\beta} * \text{area}(t_i)$', font_size=font_size)
tex_reminder_4 = Tex(r'Reminder: (4) $\text{area}(t_i) < \frac{\beta}{e^{\beta-5}} * |a_i^\prime|^2$', font_size=font_size)
tex_statement_5 = Tex(r'$\text{area}(A_i) > \frac{\lambda(2 - \lambda) * e^{\beta - 5}}{2\beta} * \text{area}(t_i)$', font_size=font_size)

tex_triangles = MyLatex([tex_green_area, tex_blue_area, tex_area_start, tex_area_middle, tex_area_end, tex_reminder_4, tex_statement_5])
