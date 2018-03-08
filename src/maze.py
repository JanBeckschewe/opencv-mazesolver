import random

import server

forward, right, backward, left = range(4)

path_dirs = [left, left, left, backward, left, left, left, right, backward, left, left, backward, forward, right,
             forward, right, forward]

full_path = []
full_path_position = 0
simple_path = []
simple_path_position = 0


def add_turn(turn):
    full_path.append([turn, random.randint(149, 150)])
    set_simplified_path()
    server.send_path()


def set_simplified_path():
    tmp_path = list(full_path)

    if len(tmp_path) < 3 or tmp_path[len(tmp_path) - 2][0] != backward:
        return

    total_angle = 0

    for x in range(1, 4):
        if tmp_path[len(tmp_path) - x][0] == right:
            total_angle += 90
        elif tmp_path[len(tmp_path) - x][0] == left:
            total_angle += 270
        elif tmp_path[len(tmp_path) - x][0] == backward:
            total_angle += 180

    total_angle = total_angle % 360

    for x in range(3):
        tmp_path.pop()

    if total_angle == 0:
        tmp_path.append([forward, 0])
    elif total_angle == 90:
        tmp_path.append([right, 0])
    elif total_angle == 180:
        tmp_path.append([backward, 0])
    elif total_angle == 270:
        tmp_path.append([left, 0])

    simple_path.clear()
    simple_path.extend(tmp_path)
