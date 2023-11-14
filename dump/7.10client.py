from scapy.layers.inet import UDP, IP
from scapy.sendrecv import send

SERVER_DST = "192.168.1.59"

msg = input("Enter your massage, and '$' in the end: ")
parts = input("Enter the amount of packets to divide: ")
if len(msg) < int(parts):
    print("You wrote a bigger number than the len of the msg so it can not divide the msg,"
          "enter again.")
    while True:
        parts = input("Enter the amount of packets to divide: ")
        if len(msg) > int(parts):
            break
else:
    i = 0
    msg_len = len(msg)
    part_len = msg_len / int(parts)
    k = int(part_len)
    part_msg = msg[:k]
    while k <= msg_len:
        for part in range(i, k):
            send(IP(dst=SERVER_DST)/UDP(dport=55555)/part_len, verbose=0)
            i += k
            k += k
            part_msg = msg[k:k+k]
            for char in part_msg:
                packet = IP(dst=SERVER_DST)/UDP(dport=55555)/char
                send(packet, verbose=0)
