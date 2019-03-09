import json, time, socket, random, datetime

sock = socket.socket()
ai = socket.getaddrinfo("127.0.0.1", 5000)
addr = ai[0][-1]
sock.connect(addr)
while True:
    data = str(sock.recv(4064))
    if(data != "b''"):
        print(data)