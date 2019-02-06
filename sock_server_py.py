#from socketio import Server as sio
import socketio

host = "0.0.0.0"
port = 8080
sio = socketio.Server()

@sio.on('connect')
def on_connect(sid, data):
    print("Connection from", sid)