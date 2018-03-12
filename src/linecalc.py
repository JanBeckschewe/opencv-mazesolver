import math


def is_line_horizontal(x1, y1, x2, y2):
    # https://www.mathebibel.de/steigungswinkel
    angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / math.pi
    return -45 < angle < 45 or 135 < angle < 180 or -180 < angle < -135


def contains_line_bottom_left(x1, y1, x2, y2, h, w):
    return (x1 < w * .3 or x2 < w * .3) and (y1 > h * .5 or y2 > h * .5)


def contains_line_bottom_right(x1, y1, x2, y2, h, w):
    return (x1 > w * .7 or x2 > w * .7) and (y1 > h * .5 or y2 > h * .5)
