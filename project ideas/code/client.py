class Clients:
    def __init__(self):
        self.db = {}

    def set_time(self, ip: str, time):
        if ip not in self.db:
            self.db[ip] = [0, 0]
        self.db[ip][1] = time

    def get_time(self, ip: str):
        return self.db.get(ip)[1]

    def set_packet_count(self, ip: str, packets_count: int):
        if ip not in self.db:
            self.db[ip] = [1, 0]
        self.db[ip][0] = packets_count

    def get_packets_count(self, ip: str):
        return self.db.get(ip)[0]

    def search(self, ip):
        if ip in self.db.keys():
            return True
        return False

    def __len__(self):
        return len(self.db.keys())

    def __str__(self):
        return "\n".join([f"{ip}: {values}" for ip, values in self.db.items()])
