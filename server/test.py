import socket
import threading
import json
import queue
import time

def server(q):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connect)
    test = {
        "type": "search",
        "name": "room"
    }
    write(s, test)
    result = read(s)
    if not result['msg']:
        test = {
            'type': 'create',
            'name': 'room',
            'address': address['server']
        }
        write(s, test)
        read(s)
        q.put(read(s))
    s.close()

def client(q):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connect)
    test = {
        "type": "search",
        "name": "room"
    }
    write(s, test)
    result = read(s)
    if result['msg']:
        test = {
            'type': 'join',
            'name': 'room',
            'address': address['client']
        }
        write(s, test)
        q.put(read(s))
    s.close()

def error (q): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connect)
    msg = {"wha": "ha ha"}
    write(s, msg)
    read(s)


def write(s, data):
    msg = json.dumps(data)
    print(msg)
    s.send(msg.encode())

def read(s):
    msg = s.recv(1024)
    print(msg.decode())
    return json.loads(msg.decode())

address = {
    'server': {'lan': '192.168.1.9', 'port':8888},
    'client': {'lan': '192.168.1.37', 'port': 54312}
}
connect = ('127.0.0.1', 8122)

q = queue.Queue()
threading.Thread(target=error, args=(q,)).start()
time.sleep(1)
cmsg = q.get()
smsg = q.get()
print(cmsg['address']['port'] == address['server']['port'])
print(smsg['address']['port'] == address['client']['port'])

