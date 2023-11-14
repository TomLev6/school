from scapy.layers.inet import TCP, IP
from scapy.sendrecv import sr1
"""
Author: Tom Lev.
Date: 05.02.22
Gets an ip address and prints the open port on the address.
"""
DST_IP = "192.168.1.22"
SRC_IP = '192.168.56.1'
SYN = 0x02  # Value in hex
ACK = 0x10  # Value in hex


def main():
    port = 20
    while port < 1025:
        sa_packet = IP(src=SRC_IP, dst=DST_IP)/TCP(dport=port, flags='S', seq=123)
        sap = sr1(sa_packet, verbose=0)
        if sap[TCP].flags & SYN and sap[TCP].flags & ACK:
            print("The port " + str(port)+" is open.")
        port += 1


if __name__ == '__main__':
    main()









