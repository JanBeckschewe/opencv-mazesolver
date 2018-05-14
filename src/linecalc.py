class LineCalc:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def is_line_horizontal(self, x1, y1, x2, y2):
        return abs(x2 - x1) > abs(y2 - y1)

    def contains_line_bottom_left(self, x1, y1, x2, y2):
        return (x1 < self.w * .1 or x2 < self.w * .1) and (y1 > self.h * .3 or y2 > self.h * .3)

    def contains_line_bottom_right(self, x1, y1, x2, y2):
        return (x1 > self.w * .9 or x2 > self.w * .9) and (y1 > self.h * .3 or y2 > self.h * .3)

    def contains_line_top(self, x1, y1, x2, y2):
        return y1 < self.w * .2 or y2 < self.w * .2

    def contains_line_bottom(self, x1, y1, x2, y2):
        return y1 >= self.w * .2 or y2 >= self.w * .2
