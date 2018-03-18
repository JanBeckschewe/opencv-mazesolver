import json
import random
import threading

import time
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

import maze

clients = []


class SocketHandler(WebSocket):

    def handleMessage(self):
        if self.data == "pause":
            maze.is_paused = True
        elif self.data == "start":
            maze.is_paused = False
        elif self.data == "reset":
            maze.full_path.clear()
            maze.simple_path.clear()
            send_path()

    def handleConnected(self):
        clients.append(self)
        send_path()

    def handleClose(self):
        clients.remove(self)


def send_path():
    print(maze.full_path[-1])
    json_object = {
        "full_path": maze.full_path,
        "simple_path": maze.simple_path,
        "path_position": maze.full_path_position
    }
    for client in clients:
        client.sendMessage(json.dumps(json_object))


def continually_append_random_turn():
    for i in range(len(maze.path_dirs)):
        maze.add_turn(maze.path_dirs[i])
    # while True:
    #     maze.add_turn(random.randint(0, 3))
        time.sleep(1)


ws_server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

threading.Thread(target=ws_server.serveforever).start()
