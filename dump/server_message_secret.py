from scapy.layers.inet import UDP, IP
import scapy.all as scapy
"""
Author: Tom Lev.
(The Server)
Gets the dport from the almost empty packet
 (no raw in it) then convert it to a letter.
 Finally prints the whole msg.
"""
SRC_IP = "192.168.1.32"


def filters(pack):
    """
    :param pack:
    :return: True or False if the request is relevant.
    """
    return UDP in pack and IP in pack and pack[IP].src == SRC_IP and\
        str(pack[UDP].dport).isdigit() and 0 < int(pack[UDP].dport) < 127


def main():
    full_msg = ""
    print("Server is up and running")
    while True:
        sn = ""
        sn = scapy.sniff(lfilter=filters, count=1)
        for packet in sn:
            msg = packet[UDP].dport
            msg = chr(msg)
            full_msg += msg
        if "$" in full_msg:
            break
    print("The message from the client: " + full_msg)
    print("The message: " + full_msg.replace("$", " "))


if __name__ == '__main__':
    main()
