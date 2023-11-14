import scapy.all as scapy
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send, sr1

tracert_pack = IP(ttl=1, dst="www.google.com") / ICMP()
tracert_pack.show()
answer = sr1(tracert_pack, verbose=0)

print("the first router is: " + answer[IP].src)  # The first router is the default gateway!

tracert_pack2 = IP(ttl=2, dst="www.google.com") / ICMP()
answer2 = sr1(tracert_pack2, verbose=0)

print("the second router is: " + answer2[IP].src)
