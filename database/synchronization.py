import multiprocessing
import threading
from data_to_file import DataFile


class Sync:
    def __init__(self, db, initializer):
        super().__init__()
        self.initializer = initializer
        self.dict = db
        self.set_ready = True
        if self.initializer:  # threading
            self.lock = threading.Lock()  # lock for def that only one person can access the database
            self.semaphore = threading.Semaphore(10)  # semaphore for multiple person access
        else:  # processing
            self.lock = multiprocessing.Lock()
            self.semaphore = multiprocessing.Semaphore(10)

    def set_value(self, key, val):
        self.lock.acquire()
        if self.set_ready:
            self.dict[key] = val
        self.lock.release()

    def get_value(self, key):
        self.semaphore.acquire()
        self.semaphore.release()
        return self.dict.get(key)

    def delete_value(self, key):
        self.lock.acquire()
        val = self.get_value(key)
        self.set_value(key, None)
        self.lock.release()
        return val

    def __str__(self):
        for key in self.dict.keys():
            return "key: " + key \
                   + "\nvalue: " + self.get_value(key)


def main():
    db = DataFile
    syndb = Sync(db, True)


# mode = Sync("threading")
