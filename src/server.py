import json
import random
import threading

import time
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

import maze

clients = []


class SocketHandler(WebSocket):
    i = 0

    def handleMessage(self):
        if self.data == "stop":
            print("stop")
        elif self.data == "start":
            print("start")

    def handleConnected(self):
        clients.append(self)
        send_path()

    def handleClose(self):
        clients.remove(self)


def send_path():
    print("send")
    json_object = {
        "full_path": maze.full_path,
        "simple_path": maze.get_simplified_maze(),
        "path_position": maze.full_path_position
    }
    for client in clients:
        client.sendMessage(json.dumps(json_object))


def continually_append_random_turn():
    while True:
        maze.add_turn(random.randint(0, 3))
        time.sleep(1)


ws_server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

threading.Thread(target=ws_server.serveforever).start()
