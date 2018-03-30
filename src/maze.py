import random
import time

import ws_server

is_paused = False

forward, right, backward, left = range(4)

path_dirs = [forward, right, left, backward, left]

full_path = []
full_path_position = 0
simple_path = []
simple_path_position = 0

time_last_turn = time.time()


def add_turn(turn):
    global time_last_turn
    turn_with_time = [turn, int((time.time() - time_last_turn) * 1000)]
    time_last_turn = time.time()
    full_path.append(turn_with_time)
    simple_path.append(turn_with_time)
    simplify_path()
    ws_server.send_path()


def simplify_path():
    if len(simple_path) < 3 or simple_path[-2][0] != backward:
        return

    total_angle = 0

    for x in range(1, 4):
        total_angle += simple_path[-x][0]

    new_turn = total_angle % 4

    length = simple_path[-1][1]

    for x in range(3):
        simple_path.pop()

    simple_path.append([new_turn, length])


def reset():
    global time_last_turn
    full_path.clear()
    simple_path.clear()
    time_last_turn = time.time()
