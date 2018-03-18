import random

import server

is_paused = False

forward, right, backward, left = range(4)

path_dirs = [left, left, left, backward, left, left, left, right, backward, left, left, backward, forward, right,
             forward, right, forward]

full_path = []
full_path_position = 0
simple_path = []
simple_path_position = 0


def add_turn(turn):
    turn_with_time = [turn, random.randint(149, 150)]
    full_path.append(turn_with_time)
    simple_path.append(turn_with_time)
    simplify_path()
    server.send_path()


def simplify_path():
    if len(simple_path) < 3 or simple_path[len(simple_path) - 2][0] != backward:
        return

    total_angle = 0

    for x in range(1, 4):
        if simple_path[len(simple_path) - x][0] == right:
            total_angle += 90
        elif simple_path[len(simple_path) - x][0] == left:
            total_angle += 270
        elif simple_path[len(simple_path) - x][0] == backward:
            total_angle += 180

    total_angle = total_angle % 360

    for x in range(3):
        simple_path.pop()

    if total_angle == 0:
        simple_path.append([forward, 0])
    elif total_angle == 90:
        simple_path.append([right, 0])
    elif total_angle == 180:
        simple_path.append([backward, 0])
    elif total_angle == 270:
        simple_path.append([left, 0])
