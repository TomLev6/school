"""
Author: Tom Lev
Date: 22/11/22
"""
from multiprocessing import Process
from synchronization import Sync
from data_to_file import DataFile

FILE_NAME = "database.bin"


def main():
    """
     calls the reader and the writer methods.
     using processing.
     :return: None
     """
    db = DataFile(FILE_NAME)
    s = Sync(db, False)
    procs = []
    for _ in range(10):
        proc = Process(target=writer_check, args=(s,))
        proc.start()
        proc2 = Process(target=reader_check, args=(s,))
        proc2.start()
        procs.append(proc)
        procs.append(proc2)
    for proc in procs:
        proc.join()


def reader_check(db):
    """
    checks if the value natch the key.
    param db: object
    :return: None
    """
    for i in range(1000):
        assert (i == db.get_value(i))


def writer_check(db):
    """
    checks if the value natch the key.
    param db: object
    :return: None
    """
    for i in range(1000):
        assert db.set_value(i, i)


if __name__ == '__main__':
    main()
