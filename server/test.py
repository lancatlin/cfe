import socket
import threading
import json

def newConnect(num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8001))
    test = {
        "name": "client",
        "id": num,
        "address": s.getsockname()
    }
    s.send(json.dumps(test).encode())
    msg = s.recv(1024)
    print(json.loads(msg.decode()))
    s.close()

for i in range(100):
    threading.Thread(target=newConnect, args=(i,)).start()
