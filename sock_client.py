import socket
import time
import ssl

def main():
    s = socket.socket()

    ai = socket.getaddrinfo("127.0.0.1", 8080)
    print("Address infos:", ai)
    addr = ai[0][-1]
    print("Connect address:", addr)
    s.connect(addr)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    secure_sock = context.wrap_socket(s)
    cert = secure_sock.getpeercert()
    print ("cert~", cert)
    while True:
    	data = secure_sock.recv(4096)
        if(data[0] == ""):
            break
        else:
            print data 
    secure_sock.close()


main()
