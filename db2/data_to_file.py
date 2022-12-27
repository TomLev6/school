"""
Author: Tom Lev
Date: 22/11/22
"""
from database import Database
import os
from pickle import dumps, loads


class DataFile(Database):
    def __init__(self, filename):
        """
        init function, gets the file path
        :param filename: str
        """
        super().__init__()
        self.f = filename
   

    def write(self):
        """
        write methode, open the known file for writing
        then updates the data to the file then close him.
        :return: None
        """
        if os.path.isfile(self.f):

            file = win32file.CreateFileW(self.f, win32file.GENERIC_WRITE, 0, None, win32file.CREATE_ALWAYS, 0, None)
            win32file.WriteFile(file, dumps(self.dict))
            win32file.UpdateResource(file)  
            win32file.CloseHandle(file)
         else:
            raise Exception('a problem occoured, file not found!')
               

    def read(self):
        """
        read methode, open the known file dor reading
        then transfers the data to the dict object then closes the file.
        :return: None
        """
        if os.path.isfile(self.f):
            file = win32file.CreateFileW(self.f, win32file.GENERIC_READ, win32file.FILE_SHARE_READ
                                         , None, win32file.OPEN_ALWAYS, 0, None)
            data = win32file.ReadFile(file, 100000000)
            self.dict = loads(data[1])
            win32file.CloseHandle(file)
         else:
            raise Exception('a problem occoured, file not found!')

    def set_value(self, key, val):
        """
        set value function
        :param key: int
        :param val: int
        :return: res, int
        """
        self.read()
        res = super().set_value(key, val)
        self.write()
        return res

    def get_value(self, key):
        """
        get value function.
        :param key: int
        :return: val, int
        """
        self.read()
        return super().get_value(key)

    def delete_value(self, key):
        """
        deletes the value of the given key
        :param key: int
        :return: val, int
        """
        self.read()
        res = super().delete_value(key)
        self.write()
        return res
