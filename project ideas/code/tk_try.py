from scapy.all import *
from scapy.layers.inet import TCP, IP
from scapy.packet import Packet


def like_hash(packt: Packet):
    if IP and TCP in packt.layers():
        # packt.show()
        if str(packt[TCP].flags) == "A":
            x = int(packt[TCP].seq)
            y = 640 / x + int(packt[TCP].sport) + int(packt[IP].src.split(".")[-1])
            if y + 1 == int(packt[TCP].ack):
                print("true", y)
                return True
    return False


def main():
    sniff(lfilter=like_hash, count=5, filter="tcp")


if __name__ == '__main__':
    main()
