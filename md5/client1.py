import socket
import hashlib

IP = '127.0.0.1'
PORT = 8820


def main():
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    try:
        my_socket.send("ready".encode())
        data = my_socket.recv(1024).decode()
        print("The server sent " + data)
        while True:
            start = data.split("|")[0]
            end = data.split("|")[1]
            msg = data.split("|")[2]
            if
            my_socket.send(str(md5(start, end, msg)).encode())

    except socket.error as er:
        print(str(er))


def md5(sta, end, msg):
    for i in range(int(sta.split(".")[0]), int(end.split(".")[0])):
        encrypted_msg = hashlib.md5(str(i).zfill(5).encode()).hexdigest()
        if encrypted_msg == msg:
            return i
    return 0


if __name__ == '__main__':
    main()
