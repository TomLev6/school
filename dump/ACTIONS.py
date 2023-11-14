"""
 Author: Roey Firan.
 Purpose: Gets ip from the client and prints
 back all the ports that the same ip is listening on.
 date: 5/3/22
"""

# IMPORTS
from scapy.sendrecv import sr1
from scapy.layers.inet import TCP, IP


# CONSTANTS
MAX_PORT = 1025
SRC_IP = '192.168.56.1'
DST_IP = '192.168.56.1'
# FUNCTION


def main():
    all_the_ports = []
    port_number = 20
    while port_number < MAX_PORT:
        syn_segment = IP(src=SRC_IP, dst=DST_IP)/TCP(dport=port_number, seq=123)
        syn_ack_package = sr1(syn_segment, verbose=0, timeout=2)
        if syn_ack_package is not None:
            flags = syn_ack_package[TCP].flags
            if flags == 'SA':
                all_the_ports.append(port_number)
        port_number += 1
    print(all_the_ports)


if __name__ == "__main__":
    main()
