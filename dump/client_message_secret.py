from time import sleep
from scapy.layers.inet import UDP, IP
from scapy.all import *
DST_IP = "192.168.1.59"
"""
Author: Tom Lev.
(The Client)
Sends an empty packet in the char's ord value as the dport.
"""


def main():
    msg = input("enter the message ,enter $ as the last letter: ")
    for char in msg:
        c = ord(char)
        send(IP(dst=DST_IP) / UDP(dport=c))
        sleep(0.12)


if __name__ == '__main__':
    main()
