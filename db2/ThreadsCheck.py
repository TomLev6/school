"""
Author: Tom Lev
Date: 22/11/22
"""

from synchronization import Sync
from data_to_file import DataFile
import win32event
import win32process

FILE_NAME = "database.bin"
WAITING = 2 * 1000


def main():
    """
    calls the reader and the writer methods.
     using threading.
     :return: None
     """
    db = DataFile(FILE_NAME)
    s = Sync(db)

    for _ in range(10):
        thread = win32process.beginthreadex(None, 0, writer_check, (s,), 0)
        res = win32event.WaitForSingleObject(thread[0], WAITING)
        print(f'WaitForSingleObject returned: {res}')

        thread = win32process.beginthreadex(None, 0, reader_check, (s,), 0)
        res = win32event.WaitForSingleObject(thread[0], WAITING)
        print(f'WaitForSingleObject returned: {res}')

    print(s.dict)


def reader_check(db):
    for i in range(1000):
        assert (i == db.get_value(i))


def writer_check(db):
    for i in range(1000):
        assert db.set_value(i, i)


if __name__ == '__main__':
    main()
