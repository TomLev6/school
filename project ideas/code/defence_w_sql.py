from scapy.layers.inet import IP, TCP
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
from sql_db import Odbc

packet_count = 0
max_packets = 128  # (200)
start_time = time.time()
# users_list = Clients()
# black_list = Black_client()
db = Odbc()


def handle_packets(packet: Packet):
    global packet_count, start_time
    if "IP" in str(packet.layers()):
        ip = packet[IP].src
        if not db.find_in_users(ip):
            db.insert_new_user(ip, 1, str(time.time()))
        else:
            db.update_user_data(ip, db.get_user_packets(ip) + 1)
        #     if db.get_user_packets(ip) > 128:
        #         elapsed_time = float(time.time()) - float(db.get_user_time(ip))
        #         # print(f"if {users_list.get_packets_count(ip)} > {max_packets} and {elapsed_time} < 2")
        #         if db.get_user_packets(ip) > max_packets and elapsed_time < 3:  # 1
        #             print("******************************  Attack detected!  ******************************")
        #             now = datetime.now()
        #             db.insert_to_blacklist(ip, "attacker", now)
        print("routing the request to the site...")

    else:
        print("Error!")
        pass


def like_hash(packt: Packet):
    global db
    if IP and TCP in packt.layers():
        if str(packt[TCP].flags) == "A":
            if int(packt[TCP].seq) != 0 or \
                    int(packt[TCP].sport) * int(packt[IP].src.split(".")[-1]) + 1 != int(packt[TCP].ack):
                print("******************************  Attack detected!  ******************************")
                now = datetime.now()
                db.insert_to_blacklist(packt[IP].src, "attacker", now)
        elif str(packt[TCP].flags) == "S":
            ip = IP(dst=packt[IP].src)
            tcp = TCP(seq=int(int(packt[TCP].sport) * int(packt[IP].src.split(".")[-1])))
            p = ip / tcp
            send(p, inter=.0001)
    return True


def filters(pkt: Packet):
    global db
    if IP in pkt.layers():
        # if str(pkt[IP].src) == "192.168.1.32" and str(pkt[IP].dst) == "192.168.1.5":
        if db.find_in_blacklist(pkt[IP].src):
            print(f"access denied!, blocked user({pkt[IP].src})!")
            return False
        else:
            return like_hash(pkt)


def main():
    db.connect()
    while True:
        sniff(prn=handle_packets, lfilter=filters)


if __name__ == '__main__':
    main()
