import socket
import time
from datetime import datetime

PORT = 8821
IP = "127.0.0.1"
MAX_PACKET = 1024


def current_time():
    now = datetime.now()
    the_time = now.strftime("%H:%M:%S")
    return the_time


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        start = current_time()
        my_socket.sendto('Tom'.encode(), (IP, PORT))  # sends 'Tom' to the server
        (data, remote_address) = my_socket.recvfrom(MAX_PACKET)  # receives 'hello' from the server
        print('The server sent: ' + data.decode())
        end = current_time()
        elapsed = end - start
        time.strftime("%H:%M:%S", time.gmtime(elapsed))
        break
    my_socket.close()


if __name__ == '__main__':
    main()
