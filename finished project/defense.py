"""
Author: Tom Lev
Date: 11/05/23
"""
from tkinter import messagebox
from user_gui import Tk
import tkinter as tk
import multiprocessing
from scapy.layers.inet import IP, TCP
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
from sql_db import Odbc
import logging

logging.basicConfig(filename='defense.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db = Odbc()
queue = multiprocessing.Queue(maxsize=2_000)

B = "Blacklist"
S = "ServerRequests"
A = "AllRequests"
W = "Whitelist"


def sniffs(port, ip):
    """
    sniffs with filtering function and if the packets is relevant, adds the packet to the queue.
    :return: nothing
    """
    sniff(prn=lambda p: queue.put(p), lfilter=lambda p: filters(p, port, ip))


def filters(pkt: Packet, port, server_ip):
    """
    a filter function which determined if the packet is relevant packet to the server.
    :param server_ip: str
    :param port: str
    :param pkt: Packet
    :return: bool
    """

    if IP in pkt.layers() and TCP in pkt.layers() and str(pkt[IP].dst) == server_ip:

        if not db.find_in_Requests(pkt[IP].src, A):
            db.insert_to_AllRequests(pkt[IP].src, datetime.now(), 1)
        else:
            db.add_packet(pkt[IP].src, A)
        if pkt[TCP].flags not in ["RA", "R"] and str(pkt[TCP].dport) == port:
            if not db.find_in_Requests(pkt[IP].src, S):
                db.insert_to_ServerRequests(pkt[IP].src, datetime.now(), 1)
            else:
                db.add_packet(pkt[IP].src, S)
            if not db.find_in_blacklist(pkt[IP].src):
                return True
            else:
                logging.info(f"access denied!, blocked user({pkt[IP].src})!")
    return False


def costume_filter(pkt, port: str, ip: str, server_ip):
    """
    a filter function which determined if the packet is an ack packet.
    :param server_ip: str
    :param pkt: Packet
    :param port: str
    :param ip: str
    :return: bool
    """
    if IP in pkt.layers() and TCP in pkt.layers():
        if pkt[TCP].flags == "A":
            if str(pkt[IP].src) == ip and str(pkt[IP].dst) == server_ip and str(pkt[TCP].sport) == port:
                return True
    return False


def handle_packets(server_ip):
    """
    the function that responsible on the three-way handshake and the communication between the user and the server.
    received a syn packet then sends a syn-ack packet, then received an ack packet, and sends the finale message or
    routing to a web. also before sending the finale packet to the user the server checks if the ack packet is valid
    by checking if the packet acknowledgement number is the same number that was suppose to be given + 1.
    :return: nothing
    """
    while True:
        pkt = queue.get()
        if not db.find_in_users(pkt[IP].src):
            db.insert_new_user(pkt[IP].src, datetime.now())
        if db.find_in_whitelist(pkt[IP].src):
            msg_pack = IP(dst=pkt[IP].src) / TCP(dport=pkt[TCP].sport, sport=pkt[TCP].dport) / Raw(
                load="You are not an attacker!, phew..")
            send(msg_pack, inter=.001, verbose=0)
        # supposed to be syn packet
        # 3 way handshake
        # only send things, to 'receive' use queue.get()
        if str(pkt[TCP].flags) == "S":
            logging.info("server received [S]")
            new_seq = (int(pkt[TCP].sport) * int(pkt[IP].src.split(".")[-1])) + int(pkt[TCP].seq)   # y
            ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
            tcp = TCP(dport=pkt[TCP].sport, sport=pkt[TCP].dport, flags='SA', seq=new_seq, ack=pkt[TCP].seq + 1)
            p_sa = ip / tcp
            send(p_sa, verbose=0)
            logging.info("server sent: [SA]")
            tm = datetime.now()
            a_pkt = queue.get()  # הוצאה
            while not costume_filter(a_pkt, str(pkt[TCP].sport), pkt[IP].src, server_ip) and\
                    (datetime.now() - tm).seconds < 2:
                if (datetime.now() - datetime.utcfromtimestamp(a_pkt.time)).seconds < 60:
                    queue.put(a_pkt)  # החזרה לסוף התור
                a_pkt = queue.get()
            logging.info("server received [A]")
            ip = a_pkt[IP].src
            if int(a_pkt[TCP].seq) != 0 or \
                    (int(a_pkt[TCP].sport) * int(a_pkt[IP].src.split(".")[-1])) + int(a_pkt[TCP].seq) + 1 ==\
                    int(a_pkt[TCP].ack):
                if not db.find_in_whitelist(ip):
                    logging.info(f"user {a_pkt[IP].src} added to the WhiteList!")
                    db.insert_to_whitelist(ip, datetime.now(), 1)

                    msg_pack = IP(dst=a_pkt[IP].src) / TCP(dport=a_pkt[TCP].sport, sport=a_pkt[TCP].dport) / Raw(
                        load="You are not an attacker!, phew..")
                    send(msg_pack, inter=.001, verbose=0)
        else:
            queue.put(pkt)


def db_check():
    """
    Passes every 120 seconds for all the users in users if they are on the whitelist to delete them, if not move
    them to the blacklist.
    :return: nothing
    """
    threading.Timer(10.0, db_check).start()
    logging.info("[USER CHECK...]")
    db.users_check()


def rate_limit_check(max_pc_packets, max_server_packets):
    """
    thread that checks rate, every 60 seconds makes statistics of how many requests were received, if more than the
    number of requests that we defined in advance were received, a warning will pop up to the user that he is under
    attack.
    :return: nothing
    """
    threading.Timer(30.0, rate_limit_check, args=(max_pc_packets, max_server_packets)).start()
    logging.info("[RATE LIMIT CHECK...]")
    # logging.info("TOTAL REQUESTS TO THE COMPUTER:", sum_all_requests(max_pc_packets))
    # logging.info("TOTAL REQUESTS TO THE SERVER:", sum_server_requests(max_server_packets))
    if sum_whitelist_requests(max_server_packets) > int(max_server_packets):
        logging.info("SERVER UNDER ATTACK!!!")
    if sum_all_requests(max_pc_packets) > int(max_pc_packets):
        logging.info("PC UNDER ATTACK!!!")
    if sum_server_requests(max_server_packets) > int(max_server_packets):
        logging.info("SERVER UNDER ATTACK!!!")


def sum_all_requests(max_pc_packets):
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
        if packets > int(max_pc_packets) / 10:  # if the user sends over max_packets / 10 packets to the
            # server in under 30 seconds he gets blocked

            if not db.find_in_blacklist(ip):
                db.insert_to_blacklist(ip, datetime.now())
                logging.info(f"[BLOCKING USER - {ip}]")
                threading.Thread(target=messagebox.showwarning,
                                 args=("PC Packets Rate Notifications!", f"PC max packets rate has reached by {ip}!"),
                                 daemon=True).start()

        counter += int(db.get_packets_amount(ip, A))
    db.clear_db(A)
    return counter


def sum_server_requests(max_server_packets):
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
        if packets > int(max_server_packets) / 10:  # if the user sends over max_server_packets / 10 packets to the
            # server in under 30 seconds he gets blocked
            if db.find_in_whitelist(ip):
                db.delete_user(ip, W)
            if not db.find_in_blacklist(ip):
                db.insert_to_blacklist(ip, datetime.now())
                logging.info(f"[BLOCKING USER - {ip}]")
                threading.Thread(target=messagebox.showwarning,
                                 args=("Server Packets Rate Notifications!", f"Server max packets rate has reached by"
                                                                             f" {ip}!"),
                                 daemon=True).start()

        counter += int(db.get_packets_amount(ip, S))
    db.clear_db(S)
    return counter


def sum_whitelist_requests(max_server_packets):
    """
    blocks the user if he sent too many packets and returns the amount of the packets from all the users, in the end
    clears the table in order to analyze the amount of packets only during the defined time.
    :return: int
    """
    whitelist_users = db.whitelist_request_count()
    counter = 0
    for user in whitelist_users:
        ip = str(user).split(",")[0]
        ip = ip.split("(")[-1]
        ip = ip.split("'")[1]
        packets = int(db.get_packets_amount(ip, W))
        if packets > int(max_server_packets) / 10:  # if the user sends over max_packets / 10 packets to the
            # server in under 30 seconds he gets blocked
            db.delete_user(ip, W)
            if not db.find_in_blacklist(ip):
                db.insert_to_blacklist(ip, datetime.now())

                logging.info(f"[BLOCKING USER - {ip}]")
                threading.Thread(target=messagebox.showwarning,
                                 args=("Whitelist Packets Rate Notifications!", f"PC max packets rate has reached by"
                                                                                f" {ip}!"),
                                 daemon=True).start()

        counter += int(db.get_packets_amount(ip, W))
    return counter


def unblocking():
    """
    A function which deletes the blocked users every 30 minutes.
    :return: nothing
    """
    threading.Timer(1800.0, unblocking).start()
    logging.info("[UNBLOCKING THE BLOCKED USERS!!]")
    db.clear_db(B)


def main(port, server_ip, max_pc_packets, max_server_packets):
    """
    the main function which starts all the threads.
    :return: nothing
    """
    logging.info(f"PORT:{port} , SERVER IP:{server_ip}, MAX PACKETS PC:{max_pc_packets}, "
                 f"MAX PACKETS SERVER:{max_server_packets}")
    # sniff in the background
    t = threading.Thread(target=sniffs, args=(port, server_ip))
    t.start()

    # checking the database
    db_check()

    # checking the rate limit, checking for attack
    rate_limit_check(max_pc_packets, max_server_packets)

    # handle sniffed packets
    handle_packets(server_ip)


if __name__ == '__main__':
    window = tk.Tk()
    t5 = Tk(window, main, unblocking, db)
    window.minsize(1200, 700)
    window.maxsize(1200, 700)
    window.mainloop()
