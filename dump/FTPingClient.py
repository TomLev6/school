import os
from scapy.layers.inet import IP, ICMP, TCP
from scapy.packet import Raw
from scapy.sendrecv import sr1, sniff

# SRC = "192.168.56.1"
DST_IP = "192.168.1.32"


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :type file_name: str
    :return: the file data in a string
    :rtype: bytes
    """
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as filee:
            return filee.read()


def filters(pack):
    """
    :param pack:
    :return: True or False if the request is relevant.
    """
    return ICMP in pack and IP in pack and pack[IP].src == DST_IP


def main():
    file = input("Enter the file path: ")
    while file != "$":
        if os.path.isfile(file):
            file_data = get_file_data(file)
            data_packet = IP(dst=DST_IP) / ICMP(
                type="echo-request") / Raw(load=file_data)/TCP(dport=21, seq=123)
            ans = sr1(data_packet, verbose=0, timeout=5)
            for i in range(1, 5):
                if ans is not None:
                    if ans[Raw].load is not None:
                        if ans[Raw].load is not "OK":
                            print("server don't received send again...")
                            ans = sniff(lfilter=filters, count=1, timeout=3)

            break


if __name__ == '__main__':
    main()
print("Disconnecting...")
