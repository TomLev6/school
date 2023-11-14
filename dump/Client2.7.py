import socket

PORT = 8820
CON = 1024
IP = "127.0.0.1"
"""
Author: Tom Lev
Date: 
Send one of the commands to the server.
If the server disconnected it returns the message
(The server disconnected!).
"""


def main():
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    while True:
        try:
            cmd = input("Type (Dir, Delete, Copy, Execute, Take ScreenShot, Send_Photo, Exit): ")
            while len(cmd) < 0:
                cmd = input("Type one of these (Dir, Delete, Copy, Execute, Take ScreenShot, Send_Photo, Exit):")
            my_socket.send(cmd.encode())
            data = my_socket.recv(CON).decode()
            print("The server sent: " + data)
            if cmd == "Exit":
                my_socket.close()
                exit()
        except ConnectionResetError:
            print("The server disconnected!")
            exit()


if __name__ == '_main_':
    main()
