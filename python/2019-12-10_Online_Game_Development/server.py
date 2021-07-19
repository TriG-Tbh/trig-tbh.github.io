import _thread
import socket
import sys
from _thread import start_new_thread
from player import Player
import pickle
from settings import server, port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
print("Server started - {}:{}".format(s.getsockname()[0], s.getsockname()[1]))
s.listen(2)
print("Waiting for connections...")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]



def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        
        data = pickle.loads(conn.recv(2048))
        players[player] = data
        if not data:
            print("Disconnected.")
            break
        else:
            if player == 1:
                reply = players[0]
            else:
                reply = players[1]
            print("Received: " + data)
            print("Sending: " + reply)
        conn.sendall(pickle.dumps(reply))
        

    print("Lost connection.")
    conn.close()

currentplayer = 0

while True:
    try:
        conn, addr = s.accept()
        print("New connection: {}:{}".format(addr[0], addr[1]))

        start_new_thread(threaded_client, (conn, currentplayer,))
        currentplayer += 1
    except KeyboardInterrupt:
        print("User exited script.")
        break