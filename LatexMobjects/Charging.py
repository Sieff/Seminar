from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_lemma = Tex(r'$|a_i^\prime| \leq |a_j^\prime| / (2 - \lambda)$', font_size=font_size)
tex_height = Tex(r'$\lambda |a_i^\prime| \leq \frac{\lambda}{2 - \lambda} |a_j^\prime|$', font_size=font_size)
tex_factor = Tex(r'$\frac{|a_j^\prime|}{\frac{1 - \lambda}{2 - \lambda} |a_j^\prime|} = \frac{2- \lambda}{1 - \lambda}$', font_size=font_size)
tex_h = Tex(r'$? = \frac{2- \lambda}{1 - \lambda} * \frac{\lambda}{2 - \lambda} |a_j^\prime| = \frac{\lambda}{1 - \lambda}|a_j^\prime|$', font_size=font_size)
tex_red_area = Tex(r'$= \frac{1}{2} * \frac{\lambda}{1 - \lambda}|a_j^\prime| * |a_j^\prime|$', font_size=font_size)
tex_red_area2 = Tex(r'$= \frac{\lambda}{2(1 - \lambda)}|a_j^\prime|^2$', font_size=font_size)
tex_red_area3 = Tex(r'$\overset{(5)}{=} \frac{1}{(1 - \lambda)(2 - \lambda)}\text{area}(A_j)$', font_size=font_size)
tex_reminder_5 = Tex(r'Reminder: (5) $\frac{2}{\lambda(2- \lambda)} \text{area}(A_i) =  |a_i^\prime|^2$', font_size=font_size)

tex_charging = MyLatex([tex_lemma, tex_height, tex_factor, tex_h, tex_red_area, tex_red_area2, tex_red_area3, tex_reminder_5])
