"""
Tom Lev
22/10/22
"""
import socket
import hashlib
import os
import threading
import logging

IP = '127.0.0.1'
PORT = 8820
LEN = 8
threads = []
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
            logging.debug("The server sent " + data)
            if "FOUND" not in data:
                global free_cpus, plus, ends, mid, starts, total_cpu
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
                        threads.append(thread)
                        logging.debug(f"starting thread number {total_cpu - free_cpus}..")
                        my_socket.send(ANSWER.encode())
                        starts = 0
                        mid = 0
                        ends = 0
                        plus = 1 + starts
                        break
                    if free_cpus == 0:
                        logging.debug("waits for the threads to end..")
                        for thread in threads:
                            thread.join()
                        free_cpus = total_cpu
                    break

            else:
                logging.info("found the message!\n disconnecting...")
                my_socket.close()
                exit()
    except socket.error as er:
        logging.error(str(er))
        logging.info("disconnecting...")
        exit()
    finally:
        my_socket.close()
        exit()


def md5(sta, end, msg):
    """
    the md5 action.
    :param sta: int
    :param end: int
    :param msg: str
    :return: None
    """
    global ANSWER
    for i in range(int(sta.split(".")[0]), int(end.split(".")[0])):
        encrypted_msg = hashlib.md5(str(i).zfill(LEN).encode()).hexdigest()
        if encrypted_msg == str(msg):
            logging.info("FOUND THE MESSAGE!")
            ANSWER = str(i)


def give_range(start, end):
    """
    gives range to the client threads.
    :param start: int
    :param end: int
    :return: start and mid
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
    logging.basicConfig(filename="md5_client_log.txt", encoding='utf-8', level=logging.DEBUG)
    main()
