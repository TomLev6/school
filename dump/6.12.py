from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import sr1
"""
Author: Tom Lev.
Date: 05.02.22
Gets a domain (url) and returns his ip.
"""
IP_dst = "8.8.8.8"


def main():
    domain = ""
    while domain != "exit":
        domain = input("Enter the requested domain: ")
        if domain != "exit":
            pass
        else:
            print("disconnecting...")
            break
        dns_p = IP(dst=IP_dst)/UDP(dport=53)/DNS(qdcount=1)/DNSQR(qname=domain)
        response_packet = sr1(dns_p, verbose=0)
        s = response_packet[DNSRR].rdata
        s = str(s)
        tmp = s.split(".")[0]
        print("\r\n")
        if tmp.isdigit():
            print("The requested IP[1]:", s)
        else:
            s = response_packet[DNSRR].summary
            s = str(s)
            ip = s.split("rdata=")[-1]
            ip = ip.split(" ")[0]
            print("The requested IP[2]:", ip)
            print("\r\n")
            print("Enter another one, or type exit, ")


if __name__ == '__main__':
    main()
# domains:
# web.whatsapp.com
# www.google.com
# classroom.google.com
# data.cyber.org.il
# translate.google.com
# www.facebook.com
# stackoverflow.com
