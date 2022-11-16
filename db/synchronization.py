import multiprocessing
import threading


class Sync:
    def __init__(self, db, mode):
        super().__init__()
        self.mode = mode
        self.dict = db
        self.available = True
        if self.mode:  # threading
            self.lock = threading.Lock()  # lock for only one person can access the database
            self.semaphore = threading.Semaphore(10)  # semaphore for multiple person access
        else:  # processing
            self.lock = multiprocessing.Lock()
            self.semaphore = multiprocessing.Semaphore(10)

    def set_value(self, key, val):
        self.lock.acquire()
        if self.available:
            self.available = False
            self.dict.set_value(key, val)
        self.lock.release()

    def get_value(self, key):
        self.semaphore.acquire()
        val = self.dict.get_value(key)
        self.semaphore.release()
        return val

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


# def main():
#     db = DataFile
#     syndb = Sync(db, True)
#
#
# # mode = Sync("threading")
