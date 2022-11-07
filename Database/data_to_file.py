from database import Database
import os


class DataFile:
    def __init__(self, file):
        self.f = file
        self.free = True

    def write(self, data):
        if os.path.isfile(self.f):
            if self.free:
                self.free = False
                file = open(self.f, "a")
                file.write(data + '\n')
                file.close()

    def read(self):
        if os.path.isfile(self.f):
            if self.free:
                file = open(self.f, "r")
                print(file.read())
                file.close()

