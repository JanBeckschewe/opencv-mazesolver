class LineCalc:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def is_line_horizontal(self, x1, y1, x2, y2):
        return abs(x2 - x1) > abs(y2 - y1)

    def contains_line_left_area(self, x1, y1, x2, y2):
        return (x1 < self.w * .2 or x2 < self.w * .2) and (self.h * .85 > y1 > self.h * .15 or self.h * .85 > y2 > self.h * .15)

    def contains_line_side_area(self, x1, y1, x2, y2):
        return (x1 > self.w * .8 or x2 > self.w * .8) and (self.h * .85 > y1 > self.h * .35 or self.h * .85 > y2 > self.h * .35)

    def contains_line_top(self, x1, y1, x2, y2):
        return y1 < self.w * .2 or y2 < self.w * .2

    def contains_line_bottom(self, x1, y1, x2, y2):
        return y1 >= self.w * .2 or y2 >= self.w * .2
