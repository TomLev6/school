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


a = Attacker("192.168.1.5", 10000)
a.send_packets()

from scapy.all import *
from scapy.layers.inet import IP, TCP

target_IP = '192.168.1.5'
while True:
    IP1 = IP(dst=target_IP)
    TCP1 = TCP(dport=8000, sport=28588, flags="S")
    syn_pkt = IP1 / TCP1
    answer = sr1(syn_pkt, inter=.0001, timeout=10, verbose=0)
    if answer is not None:
        answer.show()
        ack_pkt = IP1 / TCP(dport=28588, flags="A", ack=answer[TCP].seq + 1)
        last_ans = sr1(ack_pkt, inter=.001)
        print(str(last_ans[Raw].load))


