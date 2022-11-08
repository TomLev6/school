from database import Database
from data_to_file import DataFile
import threading
import socket

IP = "0.0.0.0"
PORT = 8820
FILE_LOCATION = "D:\-tom\databasef.txt"
in_write = False
threads = []
MAX = 1024


def main():
    """
    creates threads for any client that connects to the server,
     and send him to the handle_client def.
    :return: None
    """
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    global in_write
    while True:
        try:
            while not in_write:
                client_socket, client_address = server_socket.accept()
                print("Client connected")
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                thread.start()
                threads.append(thread)
            # if in_write:
            #     for thread in threads:
            #         thread.join()
        except socket.error as e:
            print(str(e))


def handle_client(client_socket):
    """
    handles the current client
    :param client_socket: socket
    :return: None
    """
    global in_write
    try:
        while True:
            msg = client_socket.recv(MAX).decode()
    except socket.error as e:
        print(str(e))

    # print(d)
    # d.set_value("name", "yon")
    # print(d)


if __name__ == '__main__':
    main()
