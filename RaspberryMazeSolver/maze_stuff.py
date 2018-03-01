path = []
forward, right, backward, left = range(4)


def simplify_maze(turn):
    if len(path) < 3 or path[len(path) - 2] != backward:
        return

    total_angle = 0

    for x in range(1, 3):
        if path[len(path) - x] == right:
            total_angle += 90
        elif path[len(path) - x] == left:
            total_angle += 270
        elif path[len(path) - x] == backward:
            total_angle += 180

    total_angle = total_angle % 360
    path.pop(2)

    if total_angle == 0:
        path[len(path) - 1] = forward
    elif total_angle == 90:
        path[len(path) - 1] = right
    elif total_angle == 180:
        path[len(path) - 1] = backward
    elif total_angle == 270:
        path[len(path) - 1] = left
