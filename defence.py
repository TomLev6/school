from dataclasses import dataclass
from scapy.all import *
from scapy.packet import Packet

packet_count = 0
max_packets = 10
start_time = time.time()



@dataclass
class Client:
    ip: str
    packet_count: int


def custom_action(packet: Packet):

    global packet_count, start_time
    print("received packet number:", packet_count)

    # Increase the packet count
    if
    packet_count += 1

    # Check the time elapsed
    elapsed_time = time.time() - start_time

    # If more than 10 packets are received in 1 second, drop them
    if packet_count > max_packets and elapsed_time < 1:  # or b"tom" in bytes(packet)
        print("dropping packet...")

    else:
        packet.show()


# Sniff incoming packets and call custom_action() on each packet
sniff(prn=custom_action, filter="TCP and port 28588", count=1000)
