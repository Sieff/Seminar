import numpy as np
from manim import *

text_anchor = [0.3, 2.8]


class MyLatex:
    def __init__(self, texs):
        self.mobjects = texs
        self.mobject_writes = []
        for idx, m in enumerate(self.mobjects):
            if idx == 0:
                m.align_to(text_anchor, LEFT + UP)
            else:
                m.align_to(self.mobjects[idx - 1], LEFT + UP).shift(DOWN * 0.75)
            self.mobject_writes.append(Write(m))
