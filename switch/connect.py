import socket
import json
import threading

class Connect:
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.socket.settimeout(5)
        self.server = None
        self.name = None
        self.wan = self.read()['msg']
        print('wan: ' + self.wan)

    def write(self, msg):
        s = json.dumps(msg)
        self.socket.send(s.encode())

    def read(self):
        try:
            msg = self.socket.recv(1024).decode()
            s = json.loads(msg)
            if s['type'] == 'err':
                print(s['msg'])
            return s
        except socket.timeout:
            return None

    def search(self, name):
        msg = {"type": "search", "name": name}
        self.write(msg)
        return self.read()['msg']
    
    def create(self, name, address, callback):
        msg = {"type": "create", "name": name, "address": {"lan": address[0], "port": address[1]}}
        self.write(msg)
        data = self.read()
        if data['type'] == 'err':
            print(data['msg'])
            return False
        else:
            self.isServer = True
            self.name = name
            self.server = threading.Thread(target=self.receive, args=(callback,))
            self.server.start()
            return True

    def receive(self, callback):
        while self.isServer:
            try:
                data = self.read()
                if data:
                    callback(self.ipChoice(data['address']));
            except socket.error:
                self.socket.close();
                break;
        print("close Server");

    def join(self, name, address):
        msg = {"type": "join", "name": name, "address": {"lan": address[0], "port": address[1]}}
        self.write(msg)
        data = self.read()
        if data['type'] == 'err':
            return None
        self.name = name
        return self.ipChoice(data['address'])

    def close(self):
        self.socket.close()

    def ipChoice(self, address):
        if self.wan == address['wan']:
            return (address['lan'], address['port'])
        else:
            return (address['wan'], address['port'])

