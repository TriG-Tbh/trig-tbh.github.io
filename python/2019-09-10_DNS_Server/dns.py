import socket
from settings import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def getflags(flags):
    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])
    rflags = ''
    qr = '1'
    opcode = ''
    for bit in range(1, 5):
        opcode += str(ord(byte1)&(1<<bit))

    aa = '1'
    tc = '0'
    rd = '0'
    z = '000'
    rcode = '0000'

    return int(qr + opcode + aa + tc + rd, 2).to_bytes(1, byteorder='big')+int(rd+z+rcode, 2).to_bytes(1, byteorder='big')

def getquestiondomain(data):
    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            domainstring += chr(byte)
            if x == expectedlength:
                domainparts.append(domainstring)
                domainstring = ""
                state = 0
                x = 0
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            state = 1
            expectedlength = byte
        x += 1
        y += 1
    questiontype = data[y+1:y+3]

    return (domainparts, questiontype)

def buildresponse(data):
    transactionid = data[:2]
    TID = ''
    for byte in transactionid:
        TID += hex(byte)[2:]
    flags = getflags(data[2:4])
    qdcount = b'\x00\x01'
    getquestiondomain(data[12:])

while True:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    #print(data)
    sock.sendto(r, addr)