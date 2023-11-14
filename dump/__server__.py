import pickle
import socket
from threading import Thread
from __player__ import Player

"""
Author: Tom
Date: 14/3/22
Description: a multi-threaded TCP server that makes an online chat with the clients.
"""
SERVER_IP = '192.168.56.1'
MAX = 2048
QUEUE_SIZE = 4
IP = '0.0.0.0'
PORT = 8080
FORMAT = "utf-8"
FPS = 60
current_player = 0
players = [Player(200, 380, 128, 128, 330, 900, 64, 64, 1700, 300, 128, 128),
           Player(3200, 380, 128, 128, 330, 3300, 64, 64, 3700, 300, 128, 128)]


def handle_client(client_socket, player):
    """
    :param player: the client class type.
    :param client_socket: the connection socket
    handling the client.
    """
    global current_player
    client_socket.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(client_socket.recv(MAX * 4))
            players[player] = data
            if not data:
                print("disconnecting...")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("received: ", data)
                print("sending: ", reply)
            client_socket.sendall(pickle.dumps(reply))
        except socket.error or EOFError as error:
            print("error:", str(error))
            break
    print("lost connection..")
    client_socket.close()


def main():
    global current_player
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(
                    'New connection received from IP: ' + client_address[0] + '| PORT: ' + str(client_address[1]))
                thread = Thread(target=handle_client, args=(client_socket, current_player))
                thread.start()
                current_player += 1
            except socket.error as er:
                print('received socket exception - ' + str(er))
                break
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
