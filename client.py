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
print(data.decode())
uname = input()[:50]
s.sendall(uname.encode())
data = s.recv(1024)
print(data.decode())
for ix in range(5):
    question = s.recv(1024)
    print(question.decode())
    print('Provide an answer in a minute!')
    i, _, _ = select.select([sys.stdin], [], [], 10)
    if (i):
        answer = sys.stdin.readline().strip()
    else:
        print("Timeout for question #{} !".format(ix+1))
        answer = '#T'

    s.sendall(answer.encode())
    sleep(0.1)
bye = s.recv(1024)
print(bye)
s.close()
