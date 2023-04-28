import threading
import multiprocessing
from scapy.layers.inet import IP, TCP
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
from sql_db import Odbc

db = Odbc()
queue = multiprocessing.Queue(maxsize=2_000)

SERVER_IP = "192.168.1.13"
SERVER_PORT = "8909"
MAX_REQUESTS = 128 ^ 2


# TODO: TALKING CARE OF A FLOOD OF SYN REQUESTS, GUI.


def sniffs():
    sniff(prn=lambda p: queue.put(p), lfilter=filters)


def filters(pkt: Packet):
    """
    a filter function which determined if the packet is relevant packet to the server.
    :param pkt: Packet
    :return: bool
    """
    if IP in pkt.layers() and TCP in pkt.layers():
        db.insert_to_AllRequests(pkt[IP].src, datetime.now())
        if pkt[TCP].flags not in ["RA", "R"] and str(pkt[TCP].dport) == SERVER_PORT:
            db.insert_to_ServerRequests(pkt[IP].src, datetime.now())
            # if str(pkt[IP].src) == "192.168.1.32" and str(pkt[IP].dst) == "192.168.1.13" and str(pkt[TCP].dport) ==
            # "8000": #     if TCP in pkt.layers(): #         if pkt[TCP].flags not in ["RA", "R"]:
            if not db.find_in_blacklist(pkt[IP].src):
                return True
            else:
                print(f"access denied!, blocked user({pkt[IP].src})!")
    return False


def costume_filter(pkt, port: str, ip: str):
    """
    a filter function which determined if the packet is an ack packet.
    :param pkt: Packet
    :param port: str
    :param ip: str
    :return: bool
    """
    if IP in pkt.layers() and TCP in pkt.layers():
        if pkt[TCP].flags == "A":
            if str(pkt[IP].src) == ip and str(pkt[IP].dst) == SERVER_IP and str(pkt[TCP].sport) == port:
                return True
    return False


def handle_packets():
    """
    the function that responsible on the three way hand shake and the communication between the user and the server.
    received a syn packet then sends a syn-ack packet, then received an ack packet, and sends the finale message or
    routing to a web. also before sending the finale packet to the user the server checks if the ack packet is valid
    by checking if the packet acknowledgement number is the same number that was suppose to be given + 1.
    :return:
    """
    while True:
        pkt = queue.get()
        db.insert_new_user(pkt[IP].src, datetime.now())
        if db.find_in_whitelist(pkt[IP].src):
            msg_pack = IP(dst=pkt[IP].src) / TCP(dport=pkt[TCP].sport, sport=pkt[TCP].dport) / Raw(
                load="You are not an attacker!, phew..")
            send(msg_pack, inter=.001, verbose=0)

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
            a_pkt = queue.get()  # הוצאה
            while not costume_filter(a_pkt, str(pkt[TCP].sport), pkt[IP].src) and (datetime.now() - tm).seconds < 2:
                if (datetime.now() - datetime.utcfromtimestamp(a_pkt.time)).seconds < 60:
                    queue.put(a_pkt)  # החזרה לסוף התור
                a_pkt = queue.get()
            print('[A]')
            ip = a_pkt[IP].src
            if int(a_pkt[TCP].seq) != 0 or \
                    int(a_pkt[TCP].sport) * int(a_pkt[IP].src.split(".")[-1]) + 1 == int(a_pkt[TCP].ack):
                if not db.find_in_whitelist(ip):
                    db.insert_to_whitelist(ip, datetime.now())

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


def db_check():
    """
    Passes every five seconds for all the users in users if they are on the whitelist to delete them, if not move
    them to the blacklist. :return:
    """
    if datetime.now().second == 5:
        db.users_check()


def rate_limit_check():
    """
    thread that checks rate, every 60 seconds makes statistics of how many requests were received, if more than the
    number of requests that we defined in advance were received, a warning will pop up to the user that he is under
    attack. :return:
    """
    if datetime.now().second > 58:
        print("TOTAL REQUESTS TO THE COMPUTER:", db.total_request_count())
        print("TOTAL REQUESTS TO THE SERVER:", db.server_request_count())
        if db.total_request_count() > MAX_REQUESTS:
            print("UNDER ATTACK!!!")


def main():
    """
    the main function which starts all the threads.
    :return:
    """
    # sniff in the background
    t = threading.Thread(target=sniffs)
    t.start()

    # checking the database
    t2 = threading.Thread(target=db_check)
    t2.start()

    # checking the rate limit, checking for attack
    t3 = threading.Thread(target=rate_limit_check)
    t3.start()

    # handle sniffed packets
    handle_packets()


if __name__ == '__main__':
    main()
