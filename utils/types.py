from utils import utils


class Color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @property
    def hex(self):
        return utils.rgb_to_hex((self.r, self.g, self.b))

    def darken_color(self, factor=0.1):
        darken = utils.darken_color(self.r, self.g, self.b, factor=factor)
        self.r = darken[0]
        self.g = darken[1]
        self.b = darken[2]

    def __iter__(self):
        return iter([self.r, self.g, self.b])
