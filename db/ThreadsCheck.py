import random
import threading
from database import Database
from synchronization import Sync
from data_to_file import DataFile
import logging
from multiprocessing import Process

FILE_NAME = "database.bin"


def main():
    db = DataFile(FILE_NAME)
    for i in range(0, 40):
        s = Sync(db, True)
        thread = threading.Thread(target=handle_thread, args=(s, i))
        thread.start()
        # num = random.randint(1, 2)
        # if num == 1:
        #     thread = threading.Thread(target=handle_thread, args=(s, i))
        #     thread.start()
        # else:
        #     s.mode = False
        #     proc = Process(target=handle_thread, args=(s, i))
        #     proc.start()


def handle_thread(s, num):
    try:
        s.set_value(num, num)
        g = s.get_value(num)
        if g != num:
            print("Error")
        print(s.dict)
    except SystemError as er:
        logging.error(str(er))


if __name__ == '__main__':
    main()
