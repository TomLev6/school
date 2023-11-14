import socket
import threading
from threading import Thread

"""
Author: Tom
Date: 14/3/22
Description: a multi-threaded TCP server that makes an online chat with the clients.
"""

MAX = 1024
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
FORMAT = "utf-8"
clients = []
aliases = []


def broadcast(msg):
    for client in clients:
        client.send(msg)


def handle_connection(client_socket, client_address):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    try:
        print('New connection received from IP: (' + client_address[0] + ')| PORT: (' + str(client_address[1]) + ')')
        print("handling client..")
        # handle the communication
        handle_client(client_socket)
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        client_socket.close()


def handle_client(client_socket):
    """
    :param client_socket: the connection socket
    handling the client.
    """
    while True:
        try:
            msg = client_socket.recv(MAX)
            broadcast(msg)
            print(msg.decode())

        except socket.error:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            alias = aliases[index]
            broadcast(f'{alias.decode()} has left the chat room!'.encode(FORMAT))
            aliases.remove(alias)
            print("client disconnecting..")
            break
        finally:
            print(f"active connections {len(clients)}")


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            client_socket.send('alias?'.encode(FORMAT))
            alias = client_socket.recv(1024)
            aliases.append(alias)
            clients.append(client_socket)
            print(f'The alias of this client is {alias.decode()}')
            broadcast(f'{alias.decode()} has connected to the chat room '.encode(FORMAT))
            client_socket.send('you are now connected!'.encode(FORMAT))
            thread = Thread(target=handle_connection, args=(client_socket, client_address))
            thread.start()
            print(f"active connections {threading.active_count() - 1}")
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
