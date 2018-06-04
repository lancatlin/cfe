import connect
import time
from multiprocessing import Process
import os

name = 'room'
address = ('lancatserver.ddns.net', 8122)
'''
server = Process(target = os.system, args = ('nodejs app.js',))
server.start()
server.join(1)
'''
c1 = connect.Connect(address)
print(c1.search(name))
result = c1.create(name, ('server', 8877), lambda data: print(data))
print(result)
c2 = connect.Connect(address)
print(c2.search(name))
print(c2.join(name, ('client', 1234)))
time.sleep(1)
c1.close()
time.sleep(5)
print(c2.search(name))
c2.close()
#server.terminate()

