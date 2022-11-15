import threading
from database import Database
from synchronization import Sync
from data_to_file import DataFile
import logging


FILE_NAME = "database.bin"


def main():
    thread = threading.Thread((handle_thread()),)
    thread.start()


def handle_thread():
    try:
        db = DataFile(FILE_NAME)
        db.set_value("name", "Tom")
        print(db.dict)
        db.set_value("name2", "roey")
        print(db.get_value("name2"))
        print(db.dict)
    except SystemError as er:
        logging.error(str(er))


if __name__ == '__main__':
    main()
