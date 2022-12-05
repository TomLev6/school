"""
Author: Tom Lev
Date: 22/11/22
"""
import multiprocessing
# import threading
import win32event
import win32process


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
            self.locks = win32event.CreateMutex(None, False, 'Main Thread')
            # self.lock = threading.Lock()  # lock for only one person can access the database
            self.semaphores = win32event.CreateSemaphore(None, False, 'Thread')
            # self.semaphore = threading.Semaphore(10)  # semaphore for multiple person access
        else:  # processing
            self.locks = win32process.CreateProcess(None, False, 'Main Process')
            self.semaphore = win32process.CreateProcess(None, False, 'Process')
            # self.lock = multiprocessing.Lock()
            # self.semaphore = multiprocessing.Semaphore(10)

    def set_value(self, key, val):
        """
        set value function
        :param key: int
        :param val: int
        :return: res
        """
        # self.lock.acquire()
        if self.mode:
            self.locks = win32event.OpenMutex(win32event.SYNCHRONIZE, False, "Main Thread")
            for i in range(10):
                self.semaphores = win32event.OpenSemaphore(None, False, 'Thread')
                # self.semaphore.acquire()
            res = self.dict.set_value(key, val)
            for i in range(10):
                win32event.ReleaseSemaphore(self.semaphores)
                # self.semaphore.release()
            win32event.ReleaseMutex(self.locks)
            # self.lock.release()
        else:
            self.locks = win32process.(win32event.SYNCHRONIZE, False, "Main Thread")
            for i in range(10):
                self.semaphores = win32event.OpenSemaphore(None, False, 'Thread')
                # self.semaphore.acquire()
            res = self.dict.set_value(key, val)
            for i in range(10):
                win32event.ReleaseSemaphore(self.semaphores)
                # self.semaphore.release()
            win32event.ReleaseMutex(self.locks)
            # self.lock.release()
        return res

    def get_value(self, key):
        """
        get value function.
        :param key: int
        :return: val, int
        """
        # self.semaphore.acquire()
        self.semaphores = win32event.OpenSemaphore(None, False, 'Thread')
        val = self.dict.get_value(key)
        win32event.ReleaseSemaphore(self.semaphores)
        # self.semaphore.release()
        return val

    def delete_value(self, key):
        """
        deletes the value of the given key
        :param key: int
        :return: val, int
        """
        # self.lock.acquire()
        self.locks = win32event.OpenMutex(win32event.SYNCHRONIZE, False, "Main Thread")
        val = self.get_value(key)
        self.set_value(key, None)
        # self.lock.release()
        win32event.ReleaseMutex(self.locks)
        return val

    def __str__(self):
        """
        print function
        :return: str
        """
        return "\n".join([f"{k}: {self.dict[k]}" for k in self.dict.keys()])
