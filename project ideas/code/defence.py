from scapy.layers.inet import IP
from client import Clients
from black_client import Black_client
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
import tkinter_gui

packet_count = 0
max_packets = 128  # (200)
start_time = time.time()
users_list = Clients()
black_list = Black_client()


def handle_packets(packet: Packet):
    global packet_count, start_time
    if "IP" in str(packet.layers()):
        ip = packet[IP].src
        if not users_list.search(ip):
            users_list.set_packet_count(ip, 1)
            users_list.set_time(ip, time.time())
        else:
            users_list.set_packet_count(ip, users_list.get_packets_count(ip) + 1)
            if users_list.get_packets_count(ip) > 128:
                # Check the time elapsed
                elapsed_time = time.time() - users_list.get_time(ip)
                # print(f"if {users_list.get_packets_count(ip)} > {max_packets} and {elapsed_time} < 2")
                if users_list.get_packets_count(ip) > max_packets and elapsed_time < 3:  # 1
                    print("******************************  Attack detected!  ******************************")
                    now = datetime.now()
                    black_list.set_mode(ip, True)
                    black_list.set_time(ip, now.strftime("%H:%M:%S"))
            else:
                # should route the request to the site
                print("routing the request to the site...")
                # print(users_list)
                if len(black_list) > 0:
                    print(black_list)
    else:
        print("Error!")
        pass


def filters(pkt: Packet):
    global black_list
    if IP in pkt.layers():
        # if pkt[IP].src == "172.16.6.69":
        if black_list.get_mode(pkt[IP].src):
            print(f"access denied!, blocked user({pkt[IP].src})!")
            return False
        return True


def main():
    sniff(prn=handle_packets, lfilter=filters)


if __name__ == '__main__':
    main()
