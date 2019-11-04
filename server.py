from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time

class Client:
    def __init__(self, conn, address, username):
        self.conn = conn
        self.state = 0
        self.username = username
        self.address = address
        self.answer = []

    def __repr__(self):
        return 'Client name: {}, address: {}'.format(self.username, self.address)

    def __str__(self):
        return self.__repr__()


class Server:
    def __init__(self, port):
        self.clients = set()
        self.questions = ['''1) Socket is an abstraction between: \n 
                            a) Program and OS \t b) OS and Network \n
                            c) Programmer and Programming Lang. \t d) All of above\n''',
                          '''2) TCP Socket can be used to implement: \n
                                a) a HTTP server \t b) an e-mail client \n
                                c) a FTP client \t d) All of above''',
                          '''3) DNS stands for ___, ____. \n
                                a) Domain Name Server/Distributing packages \t b) Domain Navigation Service/Resolving the address to an IP \n
                                c) Domain Name Server/Resolving the address to an IP \t d)Domain Navigation Service/Distributing packages''',
                          '''4) Which of the following explains the Application Layer? \n
                                a) Deals with transmission and reception of unstructured data through a physical medium. \n
                                b) Helps in establishing a session between processes of different stations.\n
                                c) Decides the physical path that should be taken by the data as per the network conditions.\n
                                d) Serves as the mediator between Users and processes of applications.''',
                          '''5) Choose the case where UDP can be handy. \n
                                a) Multimedia streaming \t b) E-mail application\n
                                c) P2P file sharing application \t d) Telnet/SSH client''']
        self.answers = [b'a', b'd', b'c', b'd', b'a']
        with socket(AF_INET, SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind(('localhost', port))
            self.socket.listen(2)
            self.listen_connections()

    def handle_client(self, conn, address):
        print('Received client with address: {}'.format(address))
        conn.sendall(b'Please provide a username\n')
        username = conn.recv(1024).decode()
        welcome_msg = 'Welcome {} \n'.format(username)
        conn.sendall(welcome_msg.encode())
        client = Client(conn, address, username)

        self.clients.add(client)
        with conn:
            for ix, question in enumerate(self.questions):
                client.conn.sendall(question.encode())
                data = client.conn.recv(2)
                if data == b'':
                    print('{} is exiting... '.format(client))
                    break
                print('Answer from {}, answer: {}, question #{}'.format(
                    client, data.decode(), ix+1))
                client.answer.append(data)
            score = sum(map(lambda tup: tup[0] == tup[1],
                            zip(self.answers, client.answer)))

            client.conn.sendall('Your score: {}/5'.format(score).encode())

        print('{} left with the score: {}/5'.format(client, score))

    def listen_connections(self):
        while True:
            conn, address = self.socket.accept()
            th = Thread(target=self.handle_client, args=(conn, address))
            th.start()

Server(8888)
