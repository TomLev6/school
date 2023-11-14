import socket

PORT = 8820
CON = 1024
IP = "127.0.0.1"
"""
Author: Tom Lev
Date: 22/10
Send one of the commands to the server.
If the server disconnected it returns the message
(The server disconnected!).
"""


def main():
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    while True:
        try:
            cmd = input("Type (time, name, rand, exit): ")
            while len(cmd) != 4:
                cmd = input("Type one of these (time, name, rand, exit):")
            my_socket.send(cmd.encode())
            data = my_socket.recv(CON).decode()
            print("The server sent: " + data)
            if cmd == "exit":
                my_socket.close()
                exit()
        except ConnectionResetError or socket.err:
            print("The server disconnected!")
            exit()


if __name__ == '__main__':
    main()