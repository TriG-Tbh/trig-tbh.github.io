import socket
from _thread import *
import sys

server = "192.168.1.147"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(1)
print("SERVER STARTED; WAITING FOR CONNECTION")


def threaded_client(conn):
    conn.send(str.encode("CONNECTED"))
    print("sent")
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("DISCONNECTED")
                break
            else:
                print("RECIEVED: ", reply)
                print("SENDING: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("CONNECTION LOST")
    conn.close()


while True:
    conn, addr = s.accept()
    print("CONNECTED TO: ", addr)

    start_new_thread(threaded_client, (conn,))
