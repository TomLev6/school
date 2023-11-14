from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, ICMP, UDP
from scapy.sendrecv import sr1
from datetime import datetime

IP_dst = "8.8.8.8"


def like6_12(url):
    """
    :param url:
    :return: the ip of the url.
    """
    dns_p = IP(dst=IP_dst) / UDP(dport=53) / DNS(qdcount=1) / DNSQR(qname=url)
    response_packet = sr1(dns_p, verbose=0)
    s = response_packet[DNSRR].rdata
    s = str(s)
    tmp = s.split(".")[0]
    if tmp.isdigit():
        return str(s)
    else:
        s = response_packet[DNSRR].summary
        s = str(s)
        ip = s.split("rdata=")[-1]
        ip = ip.split(" ")[0]
        return str(ip)


def main():
    ttl_num = 1
    domain = input("Enter the domain: ")
    print("")
    ip_list = []
    for i in range(1, 15):
        ip = like6_12(domain)
        if ip not in ip_list:
            ip_list.append(ip)
    print("ip list from the requested domain:", ip_list)
    print("")
    last_ip = ""
    while last_ip not in ip_list and ttl_num < 255:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Send Time:", current_time)
        answer = sr1(IP(ttl=ttl_num, dst=domain) / ICMP(), verbose=0, timeout=3)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Receive Time: ", current_time)
        print("%d hops away: " % ttl_num, answer.src)
        print("\r\n")
        last_ip = str(answer.src)
        ttl_num += 1

    print("reached destination!")
    print("disconnecting...")


if __name__ == '__main__':
    main()
# www.google.com
# stackoverflow.com
