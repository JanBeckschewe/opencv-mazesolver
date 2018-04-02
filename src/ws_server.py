import json
import threading

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
            maze.reset()
            send_path()

    def handleConnected(self):
        clients.append(self)
        send_path()

    def handleClose(self):
        clients.remove(self)


def send_path():
    print(maze.full_path[-1] if maze.full_path else "[]")
    json_object = {
        "full_path": maze.full_path,
        "simple_path": maze.simple_path,
        "path_position": maze.full_path_position
    }
    for client in clients:
        client.sendMessage(json.dumps(json_object))


ws_server = SimpleWebSocketServer("127.0.0.1", 9002, SocketHandler)

threading.Thread(target=ws_server.serveforever).start()
