import socket
import glob
import os
import PyAutoGUI


CON = 1024
IP = "0.0.0.0"
PORT = 8820
"""
Author: Tom Lev
Create the server and the sockets.
Returns: server_socket, client_socket, client_address.
"""


def sockets():
    server_socket = socket.s
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    return server_socket, client_socket, client_address


def direction():
    files_list = glob.glob("./C:Cyber/*.txt")
    print(files_list)


def delete(filelocation):
    os.remove(filelocation)


#def copy():
    #shutil.copy("C:\1.txt’, r’C:\2.txt")


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
            if data == "Dir":
                assert data == "Dir"
                client_socket.send(direction().encode())
            elif data == "Delete":
                assert data == "Delete"
                location = input("Enter the location of the file: ")
                client_socket.send(delete(location).encode())
            elif data == "Copy":
                assert data == "Copy"
                client_socket.send("Copy: ".encode())
            elif data == "Execute":
                assert data == "Execute"
                client_socket.send("Executed: ".encode())
            elif data == "Take ScreenShot" or "take screenshot":
                assert data == "Take ScreenShot" or "take screenshot"
                client_socket.send("The ScreenShot: ".encode())
            elif data == "Send_Photo" or "Send Photo" or "send photo":
                assert data == "Send_Photo" or "Send Photo" or "send photo"
                client_socket.send("The Photo: ".encode())
            elif data == "Exit" or "exit":
                assert data == "Exit" or "exit"
                client_socket.close()
                server_socket.close()
                break
            else:
                client_socket.send("I don't know that command!".encode())


if __name__ == '_main_':
    main()
