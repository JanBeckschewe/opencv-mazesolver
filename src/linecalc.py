def is_line_horizontal(x1, y1, x2, y2):
    return abs(x2 - x1) > abs(y2 - y1)


def contains_line_bottom_left(x1, y1, x2, y2, h, w):
    return (x1 < w * .3 or x2 < w * .3) and (y1 > h * .5 or y2 > h * .5)


def contains_line_bottom_right(x1, y1, x2, y2, h, w):
    return (x1 > w * .7 or x2 > w * .7) and (y1 > h * .5 or y2 > h * .5)
