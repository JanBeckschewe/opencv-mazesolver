import math


def is_line_horizontal(x1, x2, y1, y2):
    # https://www.mathebibel.de/steigungswinkel
    angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / math.pi
    return -45 < angle < 45


def is_line_vertical(x1, x2, y1, y2):
    angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / math.pi
    return 60 < angle < 120


def is_line_left(x1, x2, y1, y2, h, w):
    return (x1 < w * .4 or x2 < w * .4) and (y1 > h * .5 or y2 > h * .5)


def is_line_right(x1, x2, y1, y2, h, w):
    return (x1 > w * .4 or x2 > w * .4) and (y1 > h * .5 or y2 > h * .5)
