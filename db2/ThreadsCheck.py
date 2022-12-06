"""
Author: Tom Lev
Date: 22/11/22
"""

from synchronization import Sync
from data_to_file import DataFile
import win32event

FILE_NAME = "database.bin"


def main():
    """
    calls the reader and the writer methods.
     using threading.
     :return: None
     """
    db = DataFile(FILE_NAME)
    s = Sync(db)
    threads = []

    for _ in range(10):
        thread = win32event.CreateMutex(None, False, 'Write Thread')
        win32event.OpenMutex(writer_check(db), True, "Write Thread")
        # thread = threading.Thread(target=writer_check, args=(s,))
        # thread.start()

        thread2 = win32event.CreateMutex(None, False, 'Reader Thread')
        win32event.OpenMutex(reader_check(db), True, "Reader Thread")

        # thread2 = threading.Thread(target=reader_check, args=(s,))
        # thread2.start()

        threads.append(thread)
        threads.append(thread2)

    print(s.dict)
    for thread in threads:
        win32event.WaitForSingleObject(thread)


def reader_check(db):
    for i in range(1000):
        assert (i == db.get_value(i))


def writer_check(db):
    for i in range(1000):
        assert db.set_value(i, i)


if __name__ == '__main__':
    main()
