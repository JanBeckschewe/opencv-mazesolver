import math


def is_line_horizontal(x1, x2, y1, y2):
    angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / math.pi
    return -45 < angle < 45
