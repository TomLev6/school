import socket
import hashlib
import os
import threading

IP = '127.0.0.1'
PORT = 8820
cpu = os.cpu_count()
total_cpu = os.cpu_count()
ANSWER = 0

starts = 0
ends = 0
plus = 1


def main():
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    try:
        my_socket.send("ready".encode())
        data = my_socket.recv(1024).decode()
        print("The server sent " + data)
        global cpu
        global total_cpu
        while True:
            start = data.split("|")[0]
            end = data.split("|")[1]
            msg = data.split("|")[2]
            if cpu > 0:
                lis = give_range(start, end)
                st = lis[0]
                mi = lis[1]
                thread = threading.Thread(target=md5, args=(st, mi, msg,))
                cpu -= 1
                thread.start()
                my_socket.send(ANSWER)

    except socket.error as er:
        print(str(er))


def md5(sta, end, msg):
    global ANSWER
    for i in range(int(sta.split(".")[0]), int(end.split(".")[0])):
        encrypted_msg = hashlib.md5(str(i).zfill(5).encode()).hexdigest()
        if encrypted_msg == msg:
            ANSWER = i
    return


def give_range(start, end):
    global starts
    global ends
    global plus
    starts = float(start)
    ends = float(end)
    if plus > starts:
        plus = ends / total_cpu
    start += plus
    mid = start
    return mid, start


if __name__ == '__main__':
    main()
