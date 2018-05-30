import json
import threading

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

# there has to be a better way to solve this problem
ws_server_obj = None


class SocketHandler(WebSocket):

    def handleMessage(self):
        print('message rec')
        if self.data == "pause":
            ws_server_obj.maze.is_paused = True
        elif self.data == "start":
            ws_server_obj.maze.is_paused = False
        elif self.data == "back":
            pass
        elif self.data == "reset":
            ws_server_obj.maze.reset()
            ws_server_obj.send_path()

    def handleConnected(self):
        ws_server_obj.clients.append(self)
        ws_server_obj.send_path()

    def handleClose(self):
        ws_server_obj.clients.remove(self)


class WsServer:

    def __init__(self, maze):
        self.maze = maze
        self.clients = []
        global ws_server_obj
        ws_server_obj = self
        simple_ws_server = SimpleWebSocketServer("127.0.0.1", 9002, SocketHandler)

        threading.Thread(target=simple_ws_server.serveforever).start()

    def send_path(self):
        # print(maze.full_path[-1] if maze.full_path else "[]")
        json_object = {
            "full_path": self.maze.full_path,
            "simple_path": self.maze.simple_path,
            "path_position": self.maze.full_path_position
        }
        for client in self.clients:
            client.sendMessage(json.dumps(json_object))
