from socket import socket, AF_INET, SOCK_STREAM
from time import sleep


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
for _ in range(5):
    question = s.recv(1024)
    print(question)
    print('Provide an answer.')
    answer = input()[:2]
    s.sendall(answer.encode())
    sleep(0.1)
s.close()
