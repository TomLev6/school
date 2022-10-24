"""
Tom Lev
22/10/22
"""
import socket
import hashlib
import os
import threading

IP = '127.0.0.1'
PORT = 8820

free_cpus = os.cpu_count()
total_cpu = os.cpu_count()
ANSWER = '0'

starts = 0
mid = 0
ends = 0
plus = 1 + starts


def main():
    """
    gets the data from the server and starts threads with the md5 function ,
     returns with the 'ANSWER' to the server and requests more numbers range if the number not fount yet.
    :return: None
    """
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    try:
        while True:
            my_socket.send("ready".encode())
            data = my_socket.recv(1024).decode()
            print("The server sent " + data)
            if "FOUND" not in data:
                global free_cpus
                global total_cpu
                global starts
                global mid
                global ends
                global plus
                while True:
                    start = data.split("|")[0]
                    end = data.split("|")[1]
                    msg = data.split("|")[2]
                    while free_cpus > 0:
                        lis = give_range(int(start.split(".")[0]), int(end.split(".")[0]))
                        st = lis[0]
                        mi = lis[1]
                        thread = threading.Thread(target=md5, args=(str(st), str(mi), msg,))
                        free_cpus -= 1
                        thread.start()
                        print(f"start thread number {total_cpu - free_cpus}..")
                        my_socket.send(ANSWER.encode())
                        print("ANSWER: ", ANSWER)
                        starts = 0
                        mid = 0
                        ends = 0
                        plus = 1 + starts
                        break
                    if free_cpus == 0:
                        free_cpus = total_cpu
                    break

            else:
                print("found the message!\n disconnecting...")
                my_socket.close()
                exit()
    except socket.error as er:
        print(str(er))
    finally:
        my_socket.close()
        exit()


def md5(sta, end, msg):
    """
    the md5 action.
    :param sta: int
    :param end: int
    :param msg: str
    :return:
    """
    global ANSWER
    for i in range(int(sta.split(".")[0]), int(end.split(".")[0])):
        encrypted_msg = hashlib.md5(str(i).zfill(5).encode()).hexdigest()
        if encrypted_msg == msg:
            ANSWER = str(i)
    return 0


def give_range(start, end):
    """
    gives range to the client threads.
    :param start:
    :param end:
    :return:
    """
    global starts
    global ends
    global plus
    global mid
    mid = start
    if plus > starts:
        plus = end / total_cpu
    starts = start
    ends = end
    mid += plus
    return start, mid


if __name__ == '__main__':
    main()
