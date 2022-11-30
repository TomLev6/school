"""
Author: Tom Lev
Date: 22/11/22
"""
import threading
from synchronization import Sync
from data_to_file import DataFile

FILE_NAME = "database.bin"


def main():
    """
    calls the reader and the writer methods.
     using threading.
     :return: None
     """
    db = DataFile(FILE_NAME)
    s = Sync(db, True)
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=writer_check, args=(s,))
        thread.start()

        thread2 = threading.Thread(target=reader_check, args=(s,))
        thread2.start()
        threads.append(thread)
        threads.append(thread2)
    print(s.dict)
    for thread in threads:
        thread.join()


def reader_check(db):
    for i in range(1000):
        assert (i == db.get_value(i))


def writer_check(db):
    for i in range(1000):
        assert db.set_value(i, i)


if __name__ == '__main__':
    main()
