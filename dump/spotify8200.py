class Song:
    def __init__(self, name: str, writer: str, time: float):
        self.name = name
        self.writer = writer
        self.time = time
        self.liked = False
        self.command = None

    def __str__(self):
        return f"name: {self.name}, writer: {self.writer}, time: {self.time}"


s = Song("HELLO", "Adelle", 120.0)
print(s)
