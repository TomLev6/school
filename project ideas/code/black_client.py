class Black_client:
    def __init__(self):
        self.db = {}

    def get_all_ips(self):
        return list(self.db.keys())

    def set_time(self, ip: str, time):
        if ip not in self.db:
            self.db[ip] = [False, 0]
        self.db[ip][1] = time

    def get_time(self, ip: str):
        return self.db.get(ip)[1]

    def set_mode(self, ip: str, mode: bool):
        if ip not in self.db:
            self.db[ip] = [False, 0]
        self.db[ip][0] = mode

    def get_mode(self, ip: str):
        return self.db.get(ip)[0]

    def search(self, ip):
        if ip in self.db.keys():
            return True
        return False

    def __len__(self):
        return len(self.db.keys())

    def __str__(self):
        return "\n".join([f"{ip}: {values}" for ip, values in self.db.items()])
