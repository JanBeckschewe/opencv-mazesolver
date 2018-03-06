import json
import random
import threading
from http import server
from http.server import SimpleHTTPRequestHandler

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

import maze

path_dirs = [
    maze.forward,
    maze.forward,
    maze.right,
    maze.left,
    maze.forward,
    maze.right,
    maze.right,
    maze.forward
]
path = []

# random path with the first parameter being the directions and the second the time in milliseconds
for i in range(len(path_dirs) * 10):
    path.append([path_dirs[i % len(path_dirs)], random.randint(0, 300)])


class SocketHandler(WebSocket):
    i = 0

    def handleMessage(self):
        if self.data == "stop":
            print("stop")
        elif self.data == "start":
            print("start")

    def handleConnected(self):
        print("connected")
        self.send_path()

    def handleClose(self):
        pass

    def send_path(self):
        path.append([random.randint(0, 3), random.randint(0, 300)])
        self.sendMessage(json.dumps(path))


# not sure if I'm gonna keep that because right now it serves from the sources root directory
def run_http_server():
    server.test(HandlerClass=SimpleHTTPRequestHandler, port=80)


ws_server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

threading.Thread(target=ws_server.serveforever).start()
threading.Thread(target=run_http_server).start()

print("not serving anymore")
