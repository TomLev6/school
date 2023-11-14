from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import send, sr1
IP_dst = "8.8.8.8"
domain = ""
while domain != "exit":
    domain = input("Enter the requested domain: ")
    if domain != "exit":
        pass
    else:
        print("Closing program...")
        break
    dns_p = IP(dst=IP_dst)/UDP(sport=23333, dport=53)/DNS(qdcount=1)/DNSQR(qname=r""+domain)
    send(dns_p)
    response_packet = sr1(dns_p)
    s = response_packet[DNS].summary
    s = str(s)
    s = s.split("rdata=")[1]
    if s.isdigit():
        print("The domain: ", domain)
        print("The requested IP: ", s)
    else:
        s = response_packet[DNS].summary
        s = str(s)
        s = s.split("|")[-3]
        ip = s.split("rdata=")[1]
        print("The domain: ", domain)
        print("The requested IP: ", ip)
        print("\r\n")
        print("Enter another one, or type exit: ")
# web.whatsapp.com
# www.google.com
