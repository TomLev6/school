import threading
import multiprocessing
from scapy.layers.inet import IP, TCP
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
from sql_db import Odbc
db = Odbc()
queue = multiprocessing.Queue(maxsize=2_000)

# TODO: TALKING CARE OF A FLOOD OF SYN REQUESTS, GUI.


def sniffs():
    sniff(prn=lambda p: queue.put(p), lfilter=filters)


def filters(pkt: Packet):
    global db
    if IP in pkt.layers() and TCP in pkt.layers():
        if pkt[TCP].flags not in ["RA", "R"] and str(pkt[TCP].dport) == "8909":
            # if str(pkt[IP].src) == "192.168.1.32" and str(pkt[IP].dst) == "192.168.1.13" and str(pkt[TCP].dport) == "8000":
            # #     if TCP in pkt.layers():
            # #         if pkt[TCP].flags not in ["RA", "R"]:
            if not db.find_in_blacklist(pkt[IP].src):

                #     return False
                # else:
                return True
                # return custom_three_way_handshake(pkt)
            else:
                print(f"access denied!, blocked user({pkt[IP].src})!")  ###########
    return False


def costume_filter(pkt, port: str, ip: str):
    if IP in pkt.layers() and TCP in pkt.layers():
        if pkt[TCP].flags == "A":
            if str(pkt[IP].src) == ip and str(pkt[IP].dst) == "192.168.1.13" and str(pkt[TCP].sport) == port:
                return True
    return False


def handle_packets():
    while True:
        pkt = queue.get()
        # supposed to be syn packet
        # 3 way handshake
        # only send things, to 'receive' use queue.get()
        if str(pkt[TCP].flags) == "S":
            print("[S]")
            new_seq = (int(pkt[TCP].sport) * int(pkt[IP].src.split(".")[-1]))  # y
            ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
            tcp = TCP(dport=pkt[TCP].sport, sport=pkt[TCP].dport, flags='SA', seq=new_seq, ack=pkt[TCP].seq + 1)
            p_sa = ip / tcp
            send(p_sa, verbose=0)
            print("sent: [SA]")
            tm = datetime.now()
            a_pkt = queue.get()  #הוצאה
            while not costume_filter(a_pkt, str(pkt[TCP].sport), pkt[IP].src) and (datetime.now() - tm).seconds < 2:
                if (datetime.now() - datetime.utcfromtimestamp(a_pkt.time)).seconds < 60:
                    queue.put(a_pkt)  # החזרה לסוף התור
                a_pkt = queue.get()
            print('[A]')
            ip = a_pkt[IP].src
            if int(a_pkt[TCP].seq) == 0 or \
                    int(a_pkt[TCP].sport) * int(a_pkt[IP].src.split(".")[-1]) + 1 != int(a_pkt[TCP].ack):
                now = datetime.now()
                db.insert_to_blacklist(a_pkt[IP].src, "attacker", now)
                print("blocking..", ip)
            if not db.find_in_users(ip):
                db.insert_new_user(ip, 1, str(datetime.now()))

            msg_pack = IP(dst=a_pkt[IP].src) / TCP(dport=a_pkt[TCP].sport, sport=a_pkt[TCP].dport) / Raw(
                load="You are not an attacker!, phew..")
            send(msg_pack, inter=.001, verbose=0)
            # db.update_user_data(ip, db.get_user_packets(ip) + 1)
            #     if db.get_user_packets(ip) > 128:
            #         elapsed_time = float(time.time()) - float(db.get_user_time(ip))
            #         # print(f"if {users_list.get_packets_count(ip)} > {max_packets} and {elapsed_time} < 2")
            #         if db.get_user_packets(ip) > max_packets and elapsed_time < 3:  # 1
            #             print("******************************  Attack detected!  ******************************")
            #             now = datetime.now()
            #             db.insert_to_blacklist(ip, "attacker", now)
            # print("routing the request to the site...")
        else:
            queue.put(pkt)


def main():
    # sniff in the background
    t = threading.Thread(target=sniffs)
    t.start()
    # handle sniffed packets
    handle_packets()


if __name__ == '__main__':
    main()
    