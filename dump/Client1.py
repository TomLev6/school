import socket
import threading

PORT = 8080
CON = 1024
IP = "127.0.0.1"
FORMAT = 'utf-8'
"""
Author: Tom Lev
Date: 14/3/22
Description: a tcp client that connects to an online chat room.(broadcast)
"""

alias = input('Choose an alias >>> ')
my_socket = socket.socket()
my_socket.connect((IP, PORT))


def client_receive():
    while True:
        try:
            message = my_socket.recv(1024).decode(FORMAT)
            if message == "alias?":
                my_socket.send(alias.encode(FORMAT))
            else:
                print(message)
        except socket.error or OSError:
            print('Error!')
            my_socket.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        my_socket.send(message.encode(FORMAT))


def main():
    try:
        receive_thread = threading.Thread(target=client_receive)
        receive_thread.start()

        send_thread = threading.Thread(target=client_send)
        send_thread.start()
    except socket.error or OSError as e:
        print(str(e))


if __name__ == '__main__':
    main()
