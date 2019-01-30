import socket
import ssl
import json
import os.path

s = socket.socket()
ai = socket.getaddrinfo("0.0.0.0", 8080)
addr = ai[0][-1]
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
print("Listening on " + str(addr))
client = s.accept()
print("Connection from addr " + str(client[1]) + "!")

#Get the current directory of this file
path = os.path.dirname(os.path.abspath(__file__))
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile=os.path.join(path, "directory/to/cert", "~your-cert~.crt"),
                               keyfile=os.path.join(path, "directory/to/key", "~your-key~.key"))

secure_sock = context.wrap_socket(
    client[0], server_side=True)

try:
    secure_sock.send(json.dumps(
        {"topic": "some", "peer": "random", "sender": "data"}))
except:
    print("Lost connection to clients. Waiting for another connection...")
    client = s.accept()
