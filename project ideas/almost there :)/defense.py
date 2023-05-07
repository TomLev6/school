from user_gui import Tk
import tkinter as tk
import multiprocessing
from scapy.layers.inet import IP, TCP
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
from sql_db import Odbc
#
# import logging
# logging.basicConfig(filename='server.log', filemode="w", encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

db = Odbc()
queue = multiprocessing.Queue(maxsize=2_000)

B = "Blacklist"
S = "ServerRequests"
A = "AllRequests"
SERVER_IP = "192.168.1.13"
SERVER_PORT = "8909"
MAX_USER_REQUESTS_PC = 24000
MAX_USER_REQUESTS_SERVER = 10000


# TODO: TAKING CARE OF THE GUI.
# TODO: TRANSFER ALL THE PRINT LINES INTO A LOG FILE.


def sniffs():
    """
    sniffs with filtering function and if the packets is relevant, adds the packet to the queue.
    :return: nothing
    """
    sniff(prn=lambda p: queue.put(p), lfilter=filters)


def filters(pkt: Packet):
    """
    a filter function which determined if the packet is relevant packet to the server.
    :param pkt: Packet
    :return: bool
    """
    if IP in pkt.layers() and TCP in pkt.layers():
        if not db.find_in_Requests(pkt[IP].src, A):
            db.insert_to_AllRequests(pkt[IP].src, datetime.now(), 1)
        else:
            db.add_packet(pkt[IP].src, A)
        if pkt[TCP].flags not in ["RA", "R"] and str(pkt[TCP].dport) == SERVER_PORT:
            if not db.find_in_Requests(pkt[IP].src, S):
                db.insert_to_ServerRequests(pkt[IP].src, datetime.now(), 1)
            else:
                db.add_packet(pkt[IP].src, S)
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
    :return: nothing
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
    them to the blacklist.
    :return: nothing
    """
    threading.Timer(5.0, db_check).start()
    print("[USER CHECK...]")
    db.users_check()


def rate_limit_check():
    """
    thread that checks rate, every 60 seconds makes statistics of how many requests were received, if more than the
    number of requests that we defined in advance were received, a warning will pop up to the user that he is under
    attack.
    :return: nothing
    """
    threading.Timer(30.0, rate_limit_check).start()
    print("[RATE LIMIT CHECK...]")
    print("TOTAL REQUESTS TO THE COMPUTER:", sum_all_requests())
    print("TOTAL REQUESTS TO THE SERVER:", sum_server_requests())
    if sum_all_requests() > MAX_USER_REQUESTS_PC:
        print("PC UNDER ATTACK!!!")
    if sum_server_requests() > MAX_USER_REQUESTS_SERVER:
        print("SERVER UNDER ATTACK!!!")


def sum_all_requests():
    """
    blocks the user if he sent too many packets and returns the amount of the packets from all the users, in the end
    clears the table in order to analyze the amount of packets only during the defined time.
    :return: int
    """
    pc_users = db.total_request_count()
    counter = 0
    for user in pc_users:
        ip = str(user).split(",")[0]
        ip = ip.split("(")[-1]
        ip = ip.split("'")[1]
        packets = int(db.get_packets_amount(ip, A))
        if packets > MAX_USER_REQUESTS_SERVER / 10:  # if the user sends over 2400 packets to the
            # server in under 30 seconds he get blocked

            if not db.find_in_blacklist(ip):
                db.insert_to_blacklist(ip, datetime.now())
                print(f"[BLOCKING USER - {ip}")

        counter += int(db.get_packets_amount(ip, A))
    db.clear_db(A)
    return counter


def sum_server_requests():
    """
    blocks the user if he sent too many packets and returns the amount of the packets from all the users, in the end
    clears the table in order to analyze the amount of packets only during the defined time.
    :return: int
    """
    server_users = db.server_request_count()
    counter = 0
    for user in server_users:
        ip = str(user).split(",")[0]
        ip = ip.split("(")[-1]
        ip = ip.split("'")[1]
        packets = int(db.get_packets_amount(ip, S))
        if packets > MAX_USER_REQUESTS_SERVER / 10:  # if the user sends over 1000 packets to the
            # server in under 30 seconds he get blocked
            if not db.find_in_blacklist(ip):
                db.insert_to_blacklist(ip, datetime.now())
        counter += int(db.get_packets_amount(ip, S))
    db.clear_db(S)
    return counter


def unblocking():
    """
    A function which deletes the blocked users every 30 minutes.
    :return: nothing
    """
    threading.Timer(1800.0, unblocking).start()
    print("[UNBLOCKING THE BLOCKED USERS!!]")
    db.clear_db(B)


def main():
    """
    the main function which starts all the threads.
    :return: nothing
    """
    # sniff in the background
    t = threading.Thread(target=sniffs)
    t.start()

    # checking the database
    db_check()

    # checking the rate limit, checking for attack
    rate_limit_check()

    # releasing the blocking timeout
    # unblocking()

    # handle sniffed packets
    handle_packets()


if __name__ == '__main__':
    window = tk.Tk()
    t5 = Tk(window, main, unblocking)
    window.minsize(1200, 700)
    window.maxsize(1200, 700)
    window.mainloop()
    main()
