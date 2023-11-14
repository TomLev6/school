import socket
import datetime
import random
CON = 1024
IP = "0.0.0.0"
PORT = 8820

"""
Author: Tom Lev
Create the server and the sockets.
Returns: server_socket, client_socket, client_address.
"""


def sockets():
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    return server_socket, client_socket, client_address


"""
Gets the command from the client and display What the client ask for.
Also if the client disconnected without the command exit the server will not crush.
The server will wait for a new client.
"""


def main():
    while True:
        server_socket, client_socket, client_address = sockets()
        while True:
            try:
                data = client_socket.recv(CON).decode()
            except ConnectionResetError or OSError:
                break
            print("Client sent: " + data)
            if data == "time":
                client_socket.send(datetime.datetime.now().strftime("%H:%M:%S").encode())
            elif data == "rand":
                client_socket.send(str(random.randint(1, 10)).encode())
            elif data == "name":
                client_socket.send("Tom".encode())
            elif data == "exit":
                client_socket.close()
                server_socket.close()
                break
            else:
                client_socket.send("I don't know that command!".encode())


if __name__ == '__main__':
    main()
