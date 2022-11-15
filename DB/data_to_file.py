from database import Database
import os
from pickle import dump, load


class DataFile(Database):
    def __init__(self, filename):
        super().__init__()
        self.f = filename
        if not os.path.isfile(self.f):
            file = open(self.f, "wb")
            dump(self.dict, file)
            file.close()

    def write(self):
        if os.path.isfile(self.f):
            file = open(self.f, "wb")
            dump(self.dict, file)
            file.close()

    def read(self):
        if os.path.isfile(self.f):
            file = open(self.f, "rb")
            self.dict = load(file)
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
