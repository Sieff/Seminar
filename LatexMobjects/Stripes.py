from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_width = Tex(r'$|a_{i_1}^\prime| \leq |a_{i_1}| - |a_{i_1}^\prime| \overset{\lambda < 1}{\Leftrightarrow } \lambda |a_{i_1}^\prime| < |a_{i_1}| - |a_{i_1}^\prime|$', font_size=font_size)
tex_slope = Tex(r'$\frac{\lambda |a_{i_1}^\prime|}{|a_{i_1}| - |a_{i_1}^\prime|} \overset{\text{Lemma 3}}{\leq} \frac{\lambda |a_{i_1}^\prime|}{|a_{i_1}^\prime|} = \lambda$', font_size=font_size)
tex_reminder_l_3 = Tex(r'Reminder Lemma 3: $2|a_i^\prime|\leq |a_i|$', font_size=font_size)

tex_stripes = MyLatex([tex_width, tex_reminder_l_3, tex_slope])
