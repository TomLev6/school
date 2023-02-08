from scapy.all import *
from scapy.layers.inet import IP, TCP

target_IP = '127.0.0.1'
i = 1

while i < 100000:
    IP1 = IP(dst=target_IP)
    TCP1 = TCP(dport=28588)/Raw(load='tom')
    pkt = IP1 / TCP1
    send(pkt, inter=.0001)

    print("packet sent ", i, pkt[IP].src)
    i = i + 1
