import socket
import json
import threading

class Connect:
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.socket.settimeout(5)
        self.isServer = False
        self.name = None

    def write(self, msg):
        s = json.dumps(msg)
        self.socket.send(s.encode())

    def read(self):
        try:
            msg = self.socket.recv(1024).decode()
            s = json.loads(msg)
            return s
        except socket.timeout:
            return None
        except socket.error:
            self.isServer = False
            return None


    def search(self, name):
        msg = {"type": "search", "name": name}
        self.write(msg)
        return self.read()['msg']
    
    def create(self, name, address, callback):
        msg = {"type": "create", "name": name, "address": {"lan": address[0], "port": address[1]}}
        self.write(msg)
        data = self.read()
        if not data['msg']:
            print(data['err'])
        else:
            self.isServer = True
            self.name = name
            threading.Thread(target=self.receive, args=(callback,)).start()
        return data['msg']

    def receive(self, callback):
        while self.isServer:
            data = self.read()
            if data:
                callback(data);

    def join(self, name, address):
        msg = {"type": "join", "name": name, "address": {"lan": address[0], "port": address[1]}}
        self.write(msg)
        data = self.read()
        if data['type'] == 'err':
            return None
        addr = data['address']
        self.name = name
        return (addr['wan'], addr['port'])

    def close(self):
        self.isServer = False
        self.socket.close()

