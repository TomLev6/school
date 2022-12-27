"""
Author: Tom Lev
Date: 22/11/22
"""
import win32event
READ_NAME = 'Main Thread'
WRITE_NAME = 'Thread'

class Sync:
    def __init__(self, db):
        """
        init function
        :param db: database, object
        """
        super().__init__()
        self.dict = db
        self.locks = win32event.CreateMutex(None, False, READ_NAME)
        # lock for only one person can access the database
        self.semaphores = win32event.CreateSemaphore(None, 10, 10, WRITE_NAME)
        # semaphore for multiple person accesses

    def set_value(self, key, val):
        """
        set value function
        :param key: int
        :param val: int
        :return: res
        """
        win32event.WaitForSingleObject(self.locks, False, READ_NAME)
        for i in range(10):
            win32event.WaitForSingleObject(self.semaphores, False, WRITE_NAME)
        res = self.dict.set_value(key, val)       
        win32event.ReleaseSemaphore(self.semaphores, 10)
        win32event.ReleaseMutex(self.locks)

        return res

    def get_value(self, key):
        """
        get value function.
        :param key: int
        :return: val, int
        """
        # self.semaphore.acquire()
        win32event.WaitForSingleObject(self.semaphores, False, WRITE_NAME)
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
        win32event.WaitForSingleObject(self.locks, False, READ_NAME)
        for i in range(10):
           win32event.WaitForSingleObject(self.semaphores, False, WRITE_NAME) 
        val = self.dict.pop(key)
        win32event.ReleaseSemaphore(self.semaphores, 10)      
        win32event.ReleaseMutex(self.locks)
        return val

    def __str__(self):
        """
        print function
        :return: str
        """
        return "\n".join([f"{k}: {self.dict[k]}" for k in self.dict.keys()])
