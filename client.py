from socket import socket, AF_INET, SOCK_STREAM
from time import sleep, time
import sys
import select


class Client:
    def __init__(self, port):
        with socket(AF_INET, SOCK_STREAM) as s:
            while 22:
                self.socket = s
                self.socket.connect(('localhost', port))
                conn, addr = self.socket.accept()
                conn.sendall(b'Hellooo')
                conn.recv(1024)


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8888))
data = s.recv(1024)
print(data)
uname = input()[:50]
s.sendall(uname.encode())
data = s.recv(1024)
print(data)
for i in range(5):
    question = s.recv(1024)
    print(question)
    print('Provide an answer in a minute!')
    i, o, e = select.select([sys.stdin], [], [], 10)
    if (i):
        print("You said", sys.stdin.readline().strip())
        answer = sys.stdin.readline().strip()
    else:
        print("Timeout for question #{} !".format(i))
        answer = '#T'

    s.sendall(answer.encode())
    sleep(0.1)
bye = s.recv(1024)
print(bye)
s.close()
