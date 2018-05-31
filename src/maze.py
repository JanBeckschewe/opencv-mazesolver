import time

import ws_server


class Maze:
    def __init__(self):
        self.ws_server = ws_server.WsServer(self)

        self.is_paused = True

        self.forward, self.right, self.backward, self.left = range(4)

        self.path_dirs = [self.forward, self.right, self.left, self.backward, self.left]

        self.full_path = []
        self.full_path_position = 0
        self.simple_path = []
        self.simple_path_position = 0

        self.time_last_turn = time.time()
        self.time_when_paused = time.time()

    def get_direction_string(self, dir_num):
        dir_string = ""
        if dir_num == 0:
            dir_string = "forward"
        elif dir_num == 1:
            dir_string = "right"
        elif dir_num == 2:
            dir_string = "backwards"
        elif dir_num == 3:
            dir_string = "left"
        return dir_string

    def add_turn(self, turn):
        turn_with_time = [turn, int((time.time() - self.time_last_turn) * 1000)]
        self.time_last_turn = time.time()
        self.full_path.append(turn_with_time)
        self.simple_path.append(turn_with_time)
        self.simplify_path()
        self.ws_server.send_path()

    def pause(self):
        self.is_paused = True
        self.time_when_paused = time.time()

    def unpause(self):
        self.is_paused = False
        self.time_last_turn = time.time() - (self.time_when_paused - self.time_last_turn)

    def simplify_path(self):
        if len(self.simple_path) < 3 or self.simple_path[-2][0] != self.backward:
            return

        total_angle = 0

        for x in range(1, 4):
            total_angle += self.simple_path[-x][0]

        new_turn = total_angle % 4

        length = self.simple_path[-1][1]

        for x in range(3):
            self.simple_path.pop()

            self.simple_path.append([new_turn, length])

    def reset(self):
        self.full_path.clear()
        self.simple_path.clear()
        self.time_last_turn = time.time()
