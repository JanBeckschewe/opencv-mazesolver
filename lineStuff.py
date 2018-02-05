import math


def isLineHorizontal(x1, x2, y1, y2):
    angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / math.pi
    return -30 < angle < 60
