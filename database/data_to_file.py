from database import Database
import os
from pickle import dump, load


class DataFile(Database):
    def __init__(self, db, filename):
        super().__init__()
        self.f = filename
        self.free = True
        self.db = db

    def write(self):
        if os.path.isfile(self.f):
            if self.free:
                self.free = False
                file = open(self.f, "wb")
                dump(self.db, file)
                file.close()
                self.free = True

    def read(self):
        if os.path.isfile(self.f):
            if self.free:
                file = open(self.f, "rb")
                self.db = load(file)
                file.close()

    def set_value(self, key, val):
        self.read()
        super().set_value(key, val)
        self.write()

    def get_value(self, key):
        self.read()
        super().get_value(key)

    def delete_value(self, key):
        self.read()
        super().delete_value(key)
        self.write()
