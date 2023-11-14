from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import send

MAC = '04-D4-C4-AB-16-FF'

send(Ether(dst=MAC)/ARP(pdst="10.100.102.9/24"))
