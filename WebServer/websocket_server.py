import json
from RaspberryMazeSolver import maze_stuff

import time
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

path_dirs = [
    maze_stuff.forward,
    maze_stuff.forward,
    maze_stuff.right,
    maze_stuff.left,
    maze_stuff.forward,
    maze_stuff.forward,
    maze_stuff.forward,
    maze_stuff.forward
]
path = []

# random path with the first parameter being the directions and the second the time in milliseconds
for i in range(6):
    path.append([path_dirs[i], 100])


class SocketHandler(WebSocket):
    i = 0

    def handleMessage(self):
        # time.sleep(100)
        if self.data == "k":
            self.send_path()
            self.i += 1
            print(self.i)
        else:
            print("was anderes angekommen")

    def handleConnected(self):
        print("connected")
        self.send_path()

    def handleClose(self):
        pass

    def send_path(self):
        path.append([maze_stuff.forward, 100])
        self.sendMessage(json.dumps(path))


server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

server.serveforever()
