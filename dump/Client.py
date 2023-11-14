import socket
import io
from PIL import Image

PORT = 8080
CON = 1024
IP = "127.0.0.1"
CMD_DICT = ["dir", "delete", "copy", "execute",
            'take screenshot', "send photo", "exit"]
FOLDER_SAVE_PATH = r"C:\Cyber\tiki"
"""
Author: Tom Lev
Date: 28/12/21
Send one of the commands to the server.
If the server disconnected it returns the message
(The server disconnected!).
"""


def save_photo(folder_path, photo_bytes):
    """
    :param folder_path:
    :param photo_bytes:
    take the photo of the screenshot and save it in a known location.
    """
    photo = Image.open(io.BytesIO(photo_bytes))
    photo.save(folder_path + r"\photo27.jpg")
    # save the picture on a decided folder(^).


def show_photo(photo_bytes):
    """
    :param photo_bytes:
    shows the photo.
    """
    photo = Image.open(io.BytesIO(photo_bytes))
    photo.show()


def main():
    """
    Handles the client's requests.
    :return:
    """
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    while True:
        try:
            while True:
                cmd = input("Type one of these (Dir, Delete, Copy, Execute, "
                            "Take ScreenShot, send photo, Exit):").lower()
                if cmd in CMD_DICT:
                    pass
                else:
                    print("I don't know that command.."
                          "\ntype again or change your command"
                          " \n if the server doesn't support it.")
                    cmd = ""
                    while cmd not in CMD_DICT:
                        cmd = input("Type one of these (Dir, "
                                    "Delete, Copy, Execute, "
                                    "Take ScreenShot,"
                                    " send photo, Exit):").lower()
                if cmd.lower() == "dir":
                    my_socket.send(cmd.encode())
                    folder = input("Enter the folder path: ")
                    my_socket.send(folder.encode())
                    res = my_socket.recv(CON).decode()
                    print(res)
                elif cmd.lower() == "delete":
                    my_socket.send(cmd.encode())
                    item = input(
                        "Now write which file "
                        "the server will delete,\n"
                        "please enter the full path: ")
                    my_socket.send(item.encode())
                    print("The file has been deleted!")
                elif cmd.lower() == "copy":
                    my_socket.send(cmd.encode())
                    item = input("Write the file full path to "
                                 "copy: ")
                    my_socket.send(item.encode())
                    item2 = input("Write the file full path to "
                                  "paste: ")
                    my_socket.send(item2.encode())
                    print("The file has been copied!")
                elif cmd.lower() == "execute":
                    my_socket.send(cmd.encode())
                    application = input("Enter the full path"
                                        " of the application"
                                        " you want: ")
                    my_socket.send(application.encode())
                    print("The application is now running!")
                elif cmd.lower() == "take screenshot":
                    my_socket.send(cmd.encode())
                    print("The screenshot has been taken!")
                elif cmd.lower() == "send photo":
                    data = b""
                    my_socket.send(cmd.encode())
                    data_len = my_socket.recv(CON).decode()
                    print("received data len: " + data_len)
                    data_len = int(data_len)
                    while len(data) != data_len:
                        data += my_socket.recv(1)
                    show_photo(data)
                    save_photo(FOLDER_SAVE_PATH, data)
                    print(f"photo sent!, and saved at the known location: ({FOLDER_SAVE_PATH})")
                    print("(if case that you didn't get any photo,"
                          "\n that because you"
                          " have to take screenshot first!).")
                elif cmd.lower() == "exit":
                    my_socket.send(cmd.encode())
                    my_socket.close()
                    exit()
                    break
        except ConnectionResetError or socket.error as err:
            print("The server disconnected!" + str(err))
            exit()
        except ConnectionAbortedError as er:
            print("The server disconnected!" + str(er))
            exit()
        finally:
            print("disconnecting..")
            my_socket.close()


if __name__ == '__main__':
    main()

# ENTER A COMMAND THEN , : DIR, C:CYBER  == |||||| CMD = MSG.SPLIT(",")[0] ||||| INSIDE = MSG.SPLIT(",")[1]
