import json
import random

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

from RaspberryMazeSolver import maze_stuff

path_dirs = [
    maze_stuff.forward,
    maze_stuff.forward,
    maze_stuff.right,
    maze_stuff.left,
    maze_stuff.forward,
    maze_stuff.right,
    maze_stuff.right,
    maze_stuff.forward
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


server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

server.serveforever()
