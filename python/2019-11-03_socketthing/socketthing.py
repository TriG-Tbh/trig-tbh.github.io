import socket
host = "127.0.0.1"
port = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print(s.getsockname()[1])