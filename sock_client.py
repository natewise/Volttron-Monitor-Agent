import socket
import time

def main():
    s = socket.socket()

    ai = socket.getaddrinfo("127.0.0.1", 8080)
    print("Address infos:", ai)
    addr = ai[0][-1]
    print("Connect address:", addr)
    s.connect(addr)
    while True:
    	data = s.recvfrom(4096)
	if(data[0] == ""):
		break
	else:
		print data 
	time.sleep(4)
    s.close()


main()
