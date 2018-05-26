import socket
import threading
import json

def newConnect(num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8122))
    test = {
        "type": "search",
        "name": "room"
    }
    s.send(json.dumps(test).encode())
    msg = s.recv(1024)
    result = json.loads(msg.decode())
    if result['msg']:
        test = {
            'type': 'join',
            'name': 'room'
        }
        s.send(json.dumps(test).encode())
    else:
        test = {
            'type': 'create',
            'name': 'room'
        }
        s.send(json.dumps(test).encode())
    s.close()

newConnect(0);
newConnect(1);
for i in range(0):
    threading.Thread(target=newConnect, args=(i,)).start()
