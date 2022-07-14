from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_u = Tex(r'Let $\text{area}(t) = \beta u, u > 0$', font_size=font_size)
tex_blue_area_below = Tex(r'$= u = \frac{1}{\beta} \text{area}(t)$', font_size=font_size)
tex_green_area_below = Tex(r'$= \int_{\frac{u}{h}}^w \frac{u}{x} dx$', font_size=font_size)
tex_area_sum = Tex(r'$u + \int_{\frac{u}{h}}^w \frac{u}{x} dx = u(1 + \ln (hw) - \ln u)$', font_size=font_size)
tex_area_tile = Tex(r'$\text{area}(t) = \beta u < u(1 + \ln (hw) - \ln u)$', font_size=font_size)
tex_rearrange1 = Tex(r'$e^{\beta - 1}u < hw$', font_size=font_size)
tex_rearrange2 = Tex(r'$\beta u < \frac{\beta}{e^{\beta - 1}} hw$', font_size=font_size)
tex_rearrange3 = Tex(r'$\text{area}(t) < \frac{\beta}{e^{\beta - 1}} hw$', font_size=font_size)


tex_beta_property_proof = MyLatex([tex_u, tex_blue_area_below, tex_green_area_below, tex_area_sum, tex_area_tile,
                                   tex_rearrange1, tex_rearrange2, tex_rearrange3])
