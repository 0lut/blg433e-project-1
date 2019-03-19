from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time


class Server:
    def __init__(self, port):
        self.clients = set()
        self.questions = ['1)', '2)', '3)', '4)', '5)']
        self.answers = [b'a', b'b', b'c', b'd', b'a']
        with socket(AF_INET, SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind(('localhost', port))
            self.socket.listen(2)
            self.listen_connections()

    def handle_client(self, conn, address):
        print('Received client with address: {}'.format(address))
        conn.sendall(b'Please provide a username\n')
        username = conn.recv(1024)
        welcome_msg = 'Welcome {} \n'.format(username.decode())
        conn.sendall(welcome_msg.encode())
        client = Client(conn, username)

        self.clients.add(client)
        with conn:
            for question in self.questions:
                client.conn.sendall(question.encode())
                send_timestamp = time.time()
                data = client.conn.recv(2)
                if data == b'':
                    print('Client is exiting... ', address)
                    break
                print('Answer from client ({}):'.format(address), data.decode())
                client.answer.append(data)
            score = sum(map(lambda tup: tup[0] == tup[1],
                            zip(self.answers, client.answer)))

            client.conn.sendall('Your score: {}/5'.format(score).encode())

        print('Client ({}) left with the score: {}/5'.format(address, score))

    def listen_connections(self):
        while True:
            conn, address = self.socket.accept()
            th = Thread(target=self.handle_client, args=(conn, address))
            th.start()


class Client:
    def __init__(self, conn, username):
        self.conn = conn
        self.state = 0
        self.username = username
        self.answer = []


Server(8888)
