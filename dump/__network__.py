import socket
import pickle
MAX = 2048


class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = "192.168.56.1"
        self.port = 8080
        self.address = (self.server_socket, self.port)
        self.pos = self.connect()

    def get_pos(self):
        return self.pos

    def connect(self):
        try:
            self.client_socket.connect(self.address)
            return pickle.loads(self.client_socket.recv(MAX*4))
        except socket.error:
            pass

    def send(self, data, pick=False):
        """
        sends information to the server
        :param data: str
        :param pick: boolean if should pickle or not
        :return: str
        """
        try:
            if not pick:
                self.client_socket.send(pickle.dumps(data))
            else:
                self.client_socket.send(str.encode(data))
            reply = self.client_socket.recv(MAX * 4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)

            return reply
        except socket.error as e:
            print(e)

    def disconnect(self):
        """
         disconnects from the server
        :return: Nothing.
        """
        self.client_socket.close()
