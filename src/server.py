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
    for client in clients:
        client.sendMessage(json.dumps(maze.path))


def continually_append_random_turn():
    while True:
        maze.add_turn(random.randint(0, 3))
        time.sleep(3)


ws_server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

threading.Thread(target=ws_server.serveforever).start()

if __name__ == "__main__":
    threading.Thread(target=continually_append_random_turn()).start()
