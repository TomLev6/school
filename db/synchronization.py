"""
Author: Tom Lev
Date: 22/11/22
"""
import multiprocessing
import threading


class Sync:
    def __init__(self, db, mode):
        """
        init function
        :param db: database, object
        :param mode: bool
        """
        super().__init__()
        self.mode = mode
        self.dict = db
        if self.mode:  # threading
            self.lock = threading.Lock()  # lock for only one person can access the database
            self.semaphore = threading.Semaphore(10)  # semaphore for multiple person access
        else:  # processing
            self.lock = multiprocessing.Lock()
            self.semaphore = multiprocessing.Semaphore(10)

    def set_value(self, key, val):
        """
        set value function
        :param key: int
        :param val: int
        :return: res
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        res = self.dict.set_value(key, val)
        for i in range(10):
            self.semaphore.release()
        self.lock.release()
        return res

    def get_value(self, key):
        """
        get value function.
        :param key: int
        :return: val, int
        """
        self.semaphore.acquire()
        val = self.dict.get_value(key)
        self.semaphore.release()
        return val

    def delete_value(self, key):
        """
        deletes the value of the given key
        :param key: int
        :return: val, int
        """
        self.lock.acquire()
        val = self.get_value(key)
        self.set_value(key, None)
        self.lock.release()
        return val

    def __str__(self):
        """
        print function
        :return: str
        """
        return "\n".join([f"{k}: {self.dict[k]}" for k in self.dict.keys()])
