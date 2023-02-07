from scapy.all import *

packet_count = 0
max_packets = 10
start_time = time.time()


def custom_action(packet):
    global packet_count, start_time
    print("received packet number:", packet_count)

    # Increase the packet count
    packet_count += 1

    # Check the time elapsed
    elapsed_time = time.time() - start_time

    # If more than 10 packets are received in 1 second, drop them
    if packet_count > max_packets and elapsed_time < 1:  # or b"tom" in bytes(packet)
        print("dropping packet...")
        packet.drop()


# Sniff incoming packets and call custom_action() on each packet
sniff(prn=custom_action, filter="tcp and port 28588", count=200)
