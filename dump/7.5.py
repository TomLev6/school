from scapy.layers.inet import IP, ICMP
from scapy.packet import Raw
from scapy.sendrecv import sr1

request_packet = IP(dst="142.250.186.132") / ICMP(
    type="echo-request") / "You are the best!"  # Raw(load="You are the best!")
ans = sr1(request_packet, verbose=0)
s = ans[Raw].load
