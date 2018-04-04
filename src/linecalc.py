def is_line_horizontal(x1, y1, x2, y2):
    return abs(x2 - x1) > abs(y2 - y1)


def contains_line_bottom_left(x1, y1, x2, y2, h, w):
    return (x1 < w * .3 or x2 < w * .3) and (y1 > h * .6 or y2 > h * .6)


def contains_line_bottom_right(x1, y1, x2, y2, h, w):
    return (x1 > w * .7 or x2 > w * .7) and (y1 > h * .6 or y2 > h * .6)


def contains_line_top(x1, y1, x2, y2, h, w):
    return y1 < w * .2 or y2 < w * .2


def contains_line_bottom(x1, y1, x2, y2, h, w):
    return y1 >= w * .2 or y2 >= w * .2
