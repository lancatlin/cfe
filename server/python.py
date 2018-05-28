import socket
import select
import queue
import json

messageByte = 1024
timeout = 5

class ServerApp:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('127.0.0.1', 8001)
        self.socket.bind(address)
        self.socket.listen(5)
        self.ipList = {}
        self.input = [self.socket]  #監聽列表，先監聽本身
        self.output = []            #輸出列表
        self.message = {}          #訊息儲存列表，會放入每個socket的訊息queue

    def newConnection(self):
        new, address = self.socket.accept()
        self.input.append(new)
        self.message[new] = queue.Queue()  #新增專用訊息佇列

    def receiveData(self, s):
        message = s.recv(messageByte)
        if message:
            data = json.loads(message.decode())
            print(data)
            data["name"] = "server"
            data["address"] = self.socket.getsockname()
            self.addmsg(s, json.dumps(data))
        else:   #沒有訊息，關掉連線
            self.input.remove(s)
            self.message.pop(s)
            s.close()

    def addmsg(self, s, msg):
        string = json.dumps(s)
        self.output.append(s)
        self.message[s].put(msg)

    def start(self):
        self.socket.settimeout(timeout)
        while True:
            read, write, error = select.select(self.input, self.output, self.input, timeout)
            if not (read or write or error):    #什麼都沒有
                continue

            for s in read:
                #如果是自身，代表有新連線
                if s is self.socket:
                    self.newConnection()
                #從已知連線發送過來，將接收資料
                else:
                    self.receiveData(s)
            
            for s in write:
                msg = self.message[s].get()
                s.send(msg.encode())
                self.output.remove(s)

                    
if __name__ == '__main__':
    app = ServerApp()
    app.start()

