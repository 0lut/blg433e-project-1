import select
import socket
import sys
from time import sleep

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
