from scapy.layers.inet import IP, ICMP
from scapy.packet import Raw
from scapy.sendrecv import sr1, sr

# domain = "www.facebook.com"

"""
THE REPLY DOES NOT WORK !!!
NO ANSWER WHEN PINGING(SENDING ICMP TYPE=ECHO REQUEST)
"""


domain = input("Enter the requested domain: ")
massage = input("Enter the massage: ")
ping_packet = IP(dst=domain, ttl=10) / ICMP(type="echo-request")/Raw(load=massage)


answer = sr1(ping_packet, verbose=0, timeout=8)
data = answer[ICMP].summary
data = str(data)
data = data.split("|")[-3]
data = data.split()[-2]
data = data.split("=")[-1]
print("the id:", data)
if data == "0x0":
    print("valid id!")
    pass

# msg = answer[Raw].load
# msg = str(msg)
# print(msg[1:])
print("disconnecting...")

# iface="eth1"
# iface="wifi0"
# iface="eth2"
# iface="eth0"
# iface="enp0s3"
# iface="mon0"
# iface="ath0"



