from scapy.layers.inet import IP
from client import Clients
from black_client import Black_client
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
db.connect()


def handle_packets(packet: Packet):
    global packet_count, start_time
    if "IP" in str(packet.layers()):
        ip = packet[IP].src
        if not db.find_in_users(ip):
            db.insert_new_user(ip, 1, str(time.time()))
        else:
            db.update_user_data(ip, db.get_user_packets(ip) + 1)
            if db.get_user_packets(ip) > 128:
                # Check the time elapsed
                elapsed_time = time.time() - db.get_user_time(ip)
                # print(f"if {users_list.get_packets_count(ip)} > {max_packets} and {elapsed_time} < 2")
                if db.get_user_packets(ip) > max_packets and elapsed_time < 3:  # 1
                    print("******************************  Attack detected!  ******************************")
                    now = datetime.now()
                    db.insert_to_blacklist(ip, "attacker", now)
            else:
                # should route the request to the site
                print("routing the request to the site...")
                # print(users_list)
                # if len(black_list) > 0:
                #     print(black_list)
    else:
        print("Error!")
        pass


def filters(pkt: Packet):
    global db
    if IP in pkt.layers():
        # if pkt[IP].src == "172.16.6.69":
        if db.find_in_blacklist(pkt[IP].src):
            print(f"access denied!, blocked user({pkt[IP].src})!")
            return False
        return True


def main():
    sniff(prn=handle_packets, lfilter=filters)


if __name__ == '__main__':
    main()
    
