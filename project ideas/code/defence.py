from scapy.layers.inet import IP
from client import Clients
from scapy.all import *
from scapy.packet import Packet

packet_count = 0
max_packets = 128  # (200)
start_time = time.time()
users_list = Clients()
black_list = Clients()


def handle_packets(packet: Packet):
    global packet_count, start_time
    if "IP" in str(packet.layers()):
        ip = packet[IP].src
        if not users_list.search(ip):
            users_list.set_packet_count(ip, 1)
            users_list.set_time(ip, time.time())
        else:
            users_list.set_packet_count(ip, users_list.get_packets_count(ip) + 1)
            if users_list.get_packets_count(ip) > 10:
                # Check the time elapsed
                elapsed_time = time.time() - users_list.get_time(ip)
                # print(f"if {users_list.get_packets_count(ip)} > {max_packets} and {elapsed_time} < 2")
                if users_list.get_packets_count(ip) > max_packets and elapsed_time < 1:
                    print("******************************  Attack detected!  ******************************")
                    black_list.set_packet_count(ip, 0)
            else:
                # should route the request to the site
                print("routing the request to the site...")
                # print(users_list)
                # print(black_list)

    else:
        print("Error!")
        pass


def filters(pkt: Packet):
    global black_list
    if "TCP" in pkt and "IP" in str(pkt.layers()):
        if black_list.search(pkt[IP].src):
            print(f"access denied!, blocked user({pkt[IP].src})!")
            return False
        return True


def main():
    sniff(prn=handle_packets, lfilter=filters)


if __name__ == '__main__':
    main()

