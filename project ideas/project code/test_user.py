from scapy.all import *
from scapy.layers.inet import IP, TCP

target_IP = '192.168.1.13'


#  ip.addr == 192.168.1.5 && (tcp.port == 28588 ||  tcp.port == 8000)


def filters(pkt: Packet):
    global target_IP
    if IP in pkt.layers() and TCP in pkt.layers():
        if pkt[IP].src == target_IP:
            # if pkt[TCP].flags not in ["RA", "R"]:
            return True
    return False


def filters2(pkt: Packet):
    global target_IP
    if IP in pkt.layers() and TCP in pkt.layers():
        if pkt[IP].src == target_IP:
            if pkt[TCP].flags == "":
                return True
    return False


def sr1_ignore_rst(p: Packet, inter=.0001, verbose=False) -> Union[Packet, None]:
    answer = sr1(p, inter=inter, verbose=verbose, timeout=1)  # probably return RST + ACK from the operating system
    answer2 = sniff(count=1, lfilter=filters, timeout=1)
    if answer is not None and TCP in answer.layers() and answer[TCP].flags == "SA":
        return answer

    elif answer2 and answer is not None and TCP in answer.layers() and answer[TCP].flags in ["RA", "R"]:
        answer2 = answer2[0]
        if answer2 is not None and TCP in answer2.layers() and answer2[TCP].flags == "SA":
            return answer2
    return None


def sr1_ignore_rst_second(p: Packet, inter=.0001, verbose=False) -> Union[Packet, None]:
    answer = sr1(p, inter=inter, verbose=verbose, timeout=1)  # probably return RST + ACK from the operating system
    answer2 = sniff(count=1, lfilter=filters, timeout=1)
    if answer is not None and TCP in answer.layers():  # and answer[TCP].flags == ""
        return answer

    elif answer2 and answer is not None and TCP in answer.layers() and answer[TCP].flags in ["RA", "R"]:
        answer2 = answer2[0]
        if answer2 is not None and TCP in answer2.layers() and answer2[TCP].flags == "":
            return answer2
    return None


def main():
    while True:
        IP1 = IP(dst=target_IP)
        TCP1 = TCP(dport=8000, sport=28588, flags="S", seq=random.randint(9999, 89898))
        syn_pkt = IP1 / TCP1
        sa_pack = sr1_ignore_rst(syn_pkt)

        if sa_pack is not None:
            print(int(sa_pack[TCP].seq) + 1)
            ack_pkt = IP(dst=target_IP) / TCP(dport=syn_pkt[TCP].dport,
                                              sport=syn_pkt[TCP].sport, flags="A", ack=int(sa_pack[TCP].seq) + 1)
            print("sending...")
            last_ans = sr1(ack_pkt, verbose=0, timeout=1)
            print("sent.")

            if last_ans is not None:

                p2 = sniff(count=1, lfilter=filters, timeout=1)

                if Raw in last_ans.layers() and last_ans is not None and TCP in \
                        last_ans.layers() and last_ans[TCP].flags not in ["RA", "R"]:
                    print(p2[Raw].load.decode())
                elif p2:
                    p2 = p2[0]
                    if Raw in p2.layers():
                        print(p2[Raw].load.decode())

            else:
                print("None")
                exit()


if __name__ == '__main__':
    main()
