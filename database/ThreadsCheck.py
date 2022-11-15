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
        db = Database()
        db.set_value("name", "Tom")
        f = DataFile(db, FILE_NAME)
        print(db.dict)
        f.write()
        db.set_value("name2", "roey")
        f.read()
        print(db.dict)
    except SystemError as er:
        logging.error(str(er))


if __name__ == '__main__':
    main()
