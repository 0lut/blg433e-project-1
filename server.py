from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class Server:
    def __init__(self, port):
        self.clients = set()
        self.questions = ['1)', '2)', '3)', '4)', '5)']
        self.answers = ['a', 'b', 'c', 'd', 'a']
        with socket(AF_INET, SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind(('localhost', port))
            self.socket.listen(2)
            self.listen_connections()

    def handle_client(self, conn, address):
        print('Received client with address: {}'.format(address))
        conn.sendall(b'Please provide a username\n')
        username = conn.recv(1024)
        welcome_msg = 'Welcome {} \n'.format(str(username))
        conn.sendall(welcome_msg.encode())
        client = Client(conn, username)

        self.clients.add(client)
        with conn:
            for question in self.questions:
                client.conn.sendall(question.encode())
                data = client.conn.recv(2)
                if data == b'':
                    break
                print('Cevap geldi:', data)
                client.answer.append(data)
        print('Client left: {}'.format(address))
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
