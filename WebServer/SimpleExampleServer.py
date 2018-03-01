import json

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

path_dirs = [1, 2, 1, 0, 0, 3, 2]
path = []

# random path with the first parameter being the directions and the second the time in milliseconds
for i in range(6):
    path.append([path_dirs[i], 500])


class SocketHandler(WebSocket):
    i = 0

    def handleMessage(self):
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
        self.sendMessage(json.dumps(path))


server = SimpleWebSocketServer("0.0.0.0", 8000, SocketHandler)

server.serveforever()
