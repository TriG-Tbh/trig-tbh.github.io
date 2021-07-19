import socket
import settings

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.bind((settings.SERVER_HOST, settings.SERVER_PORT))

class Game:
    def __init__(self, players):
        self.players = players

