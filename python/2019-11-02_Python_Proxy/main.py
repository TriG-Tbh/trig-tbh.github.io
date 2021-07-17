import socket, sys
import thread

import os
import platform
def clear():
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass

clear()

try:
    listening_port = int(input("[*] Enter listening port (0-65535): "))
except KeyboardInterrupt:
    print("\n[*] User requested interrupt")
    print("[*] Closing server...")
    sys.exit(0)
except:
    print("[!] Invalid port number: " + str(listening_port))
    print("[!] Closing server...")
    sys.exit(1)

max_conn = 5
buffer_size = 8192

def start():
    try:
        print("[*] Initializing socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = ''
        if ip != "":
            nip = ip
        else:
            nip = "127.0.0.1"
        s.bind((ip, listening_port))
        s.listen(max_conn)
        print("[*] Socket binded successfully")
        print("[*] Server started successfully [ {} ]".format(nip + ":" + str(listening_port)))
    except Exception as e:
        print("[!] Unable to initalize socket: " + str(e))
        sys.exit(1)
    
    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            '''conn_string_thread = threading.Thread(target=conn_string, args=(conn,data,addr,))
            conn_string_thread.start()'''
            thread.start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            s.close()        
            print("[*] User requested interrupt")
            print("[*] Closing server...")
            sys.exit(0)

def conn_string(conn, data, addr):
    first_line = data.split("\n")[0]
    url = first_line.split(" ")[1]
    http_pos = url.find("://")
    if http_pos == -1:
        temp = url
    else:
        temp = url[(http_pos + 3):]

    port_pos = temp.find(":")

    webserver_pos = temp.find("/")

    if webserver_pos == -1:
        webserver_pos = len(temp)
    webserver = ""
    port = -1
    if port_pos == -1 or webserver_pos < port_pos:
        port = 80
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(port_pos + 1):])[:webserver_pos-port_pos- 1])
        webserver = temp[:port_pos]

    print(data)

    proxy_server(webserver, port, conn, data, addr)
    '''except Exception as e:
        print(str(e))
        pass'''

def proxy_server(webserver, port, conn, data, addr):
    print(conn)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)

        while 1:
            reply = s.recv(buffer_size)

            if len(reply) > 0:
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("[*] Request done: %s => %s <=" % (str(addr[0]), str(dar)))
            else:
                break
        s.close()
        conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)

start()