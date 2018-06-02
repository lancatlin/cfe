import socket
import json

class Connect:
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.socket.settimeout(5)

    def write(self, msg):
        s = json.dumps(msg)
        self.socket.send(s.encode())

    def read(self):
        msg = self.socket.recv(1024).decode()
        s = json.loads(msg)
        return s

    def search(self, name):
        msg = {"type": "search", "name": name}
        self.write(msg)
        return self.read()['msg']
    
    def create(self, name, address):
        msg = {"type": "create", "name": name, "address": {"lan": address[0], "port": address[1]}}
        self.write(msg)
        data = self.read()
        if not data['msg']:
            print(data['err'])
        return data['msg']

    def join(self, name, address):
        msg = {"type": "join", "name": name, "address": {"lan": address[0], "port": address[1]}}
        self.write(msg)
        data = self.read()
        addr = data['address']
        return (addr['wan'], addr['port'])

