import socket

from settings import *

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

SERVER.bind((HOST, PORT))
SERVER.listen(0)


def threaded_client(conn):
    pass


while True:
    conn, addr = SERVER.accept()
