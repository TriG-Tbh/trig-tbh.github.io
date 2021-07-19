import socket
import settings

gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    gamesocket.bind((settings.LISTHOST, settings.LISTPORT))
except OSError:
    print("There is a game list already active!")
    exit()

gamesocket.listen(0)

while True:
    