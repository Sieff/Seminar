from manim import *
from LatexMobjects.MyLatex import MyLatex

font_size = 32
tex_orange_area = Tex(r'$= \lambda(3-\lambda)/8$', font_size=font_size)
tex_green_area = Tex(r'$= 1$', font_size=font_size)
tex_blue_area = Tex(r'$= 1 + \lambda(3-\lambda)/8$', font_size=font_size)

tex_trapezoids = MyLatex([tex_orange_area, tex_green_area, tex_blue_area])
