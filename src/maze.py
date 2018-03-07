import server

forward, right, backward, left = range(4)
path = []
path_position = 0
simple_path = []
simple_path_position = 0


def add_turn(turn):
    path.append([turn, 100])
    server.send_path()


def simplify_maze():
    if len(path) < 3 or path[len(path) - 2][0] != backward:
        return

    total_angle = 0

    for x in range(1, 4):
        if path[len(path) - x][0] == right:
            total_angle += 90
        elif path[len(path) - x][0] == left:
            total_angle += 270
        elif path[len(path) - x][0] == backward:
            total_angle += 180

    total_angle = total_angle % 360

    for x in range(3):
        path.pop()

    if total_angle == 0:
        path.append([forward, 0])
    elif total_angle == 90:
        path.append([right, 0])
    elif total_angle == 180:
        path.append([backward, 0])
    elif total_angle == 270:
        path.append([left, 0])

    print(path)
