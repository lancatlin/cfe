import connect

def one():
    c = connect.Conncet()
    if c.search(name):
        print(c.join(name, ('192.168.1.9', 8888)))
    else:
        print(c.create(name, ('192.168.1.37', 8877)))


name = 'room'
address = ('127.0.0.1', 8888)
c1 = connect.Connect(address)
print(c1.search(name))
c1.create(name, ('server', 8877), lambda data: print(data))
c2 = connect.Connect(address)
print(c2.search(name))
print(c2.join(name, ('client', 1234)))

