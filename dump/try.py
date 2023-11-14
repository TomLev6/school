import math
import os
import random
import time
import timeit
from datetime import datetime

from iplookup import iplookup
import scapy
from PIL import Image
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import UDP, IP, ICMP
from scapy.packet import ls
from scapy.sendrecv import send, sr1

FOLDER_PATH = r"C:\Cyber\tiki"


def calc(total, shipping, discount):
    return (total + shipping) * discount


def emoji(msg):
    words = msg.split(" ")
    emojis = {
        ":)": "smile",
        ":(": "sad"
    }
    output = ""
    for word in words:
        output += emojis.get(word, word) + " "
    return output


# msg = input(">")
# print(emoji(name=msg, msg=msg))


class Sushi:
    def sad(self):
        print("sad")

    def __init__(self, x, y):
        self.x = x  # this.x = x
        self.y = y


# point = Sushi(10, 20)


# print(point.x)


class Person:
    def __init__(self, name):
        self.name = name

    def talk(self):
        print(f'hallo, I am {self.name}')


#
# tom = Person("Tom Lev")
# # print(tom.name)
# # tom.talk()
# bob = Person("Bob Smith")


# bob.talk()

# class Dog(Person.talk(self=)):

# import Something -> we will type: Something.function
# from Something import Function -> we will type: Function(Value)


# def find_max(numbers):
#     max_num = numbers[0]
#     for num in numbers:
#         if num > max_num:
#            max_num = num
#     return max_num


# import utils
# utils.find_max(numbers=list)
# numbers = [10, 8, 28, 31]
# print(max(numbers))
# print(find_max(numbers))


class Dice:
    def roll(self):
        cube1 = random.randint(1, 6)
        cube2 = random.randint(1, 6)
        return cube2, cube1


dice = Dice()


# print(dice.roll())
# image = pyautogui.screenshot()
# image.save()
# print(image)


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :type file_name: str
    :return: the file data in a string
    :rtype: bytes
    """
    with open(file_name, 'rb') as file:  # gets the file data in byte. rb = read bytes
        return file.read()


def send_photo(file_path):
    if os.path.isfile(file_path):  # if the file exist..
        img = Image.open(file_path)
        img.save(FOLDER_PATH + r"\photo.jpg")
    else:
        print("No such a file in directory!")


def get_len(file_path):
    """
    :param file_path:
    :return: file's length.
    :rtype: int.
    """
    length = str(len(get_file_data(file_path)))
    if length.isdigit():
        length = int(length)
        return length


def execute(application):
    while True:
        try:
            os.startfile(application)
        except FileNotFoundError or OSError as error:
            print("An error encored!" + str(error))
            break


# DNS().show()
# DNSQR().show()
# UDP().show()
# ls(UDP)
# IP(dst='8.8.8.8')/
# www.google.com
# ip = iplookup.iplookup
# domain = input("Enter the requested domain: ")
# result = ip(do)
# dns_packet = IP(dst='8.8.8.8')/UDP()/DNS(qdcount=3)/DNSQR(qname=r''+domain)
# print("---------------")
# dns_packet.show()
# print("---------------")
# ls(UDP)
# print("---------------")
# send(dns_packet)
# response_packet = sr1(dns_packet)
# response_packet.show()


import socket
# from scapy.all import *
# from scapy.layers.inet import TCP, IP
#
# syn_segment = TCP(dport=80, seq=123, flags='S')
# syn_packet = IP(dst='www.google.com')/syn_segment
# syn_ack_packet = sr1(syn_packet)
# ack_segment = ""
# ack_packet = IP(dst='www.google.com')/ack_segment
# send(ack_packet)

# ip = input("Enter the IP: ")
# port = 20
# while port < 1025:
#     a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # print("now on port: " + str(port))
#     location = (ip, port)
#     result_of_check = a_socket.connect_ex(location)
#     if result_of_check == 0:
#         print("Port is open", port)
#     port += 1
#     a_socket.close()
# a_socket.close()
# # netstat -a


# --------------------------------------------
import socket
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import UDP, IP
from scapy.packet import Raw
from scapy.sendrecv import send, sr1

# IP_0 = "127.0.0.1"
# PORT = 8820
# MAX_PACKET = 1024
# DST_IP = "192.168.1.59"
# SRC_IP = "192.168.1.22"
#
# # client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # try:
# #     while True:
# msg = input("enter a char and a space after each one: ")
# msgs = msg.split(" ")
# print(msgs)
# msg = msgs[0]
#         if len(msg) == 1:
#             pass
#         else:
#             while len(msg) != 1 and msg != "Quit":
#                 print("The len must be 1!")
#                 msg = input("enter a char: ")
#         if msg == "Quit":
#             client.sendto(msg.encode(), (IP_0, PORT))
#             break
# msg = ord(msg)
# # PORT = msg
# msg = str(msg)
# # dns_p =
# pack = IP(src=SRC_IP, dst=DST_IP) / UDP(dport=PORT) / DNS(qdcount=1) / Raw(load=msg)
# p = pack[Raw].load
# p = int(p)
# print(p)
# if dns_p[Raw].load & "":
#     print("Got it.")
# client.sendto(msg.encode(), (IP_0, PORT))
# (data, remote_address) = client.recvfrom(MAX_PACKET)
# print('The server sent: ' + data.decode())
#         print("Enter Quit if you want to exit the program.")
# except socket.error as e:
#     print(str(e))
# finally:
#     client.close()


# (client_data, client_address) = server_socket.recvfrom(MAX_PACKET)
# print("Client received: " + str(client_data))
# if client_data == "Quit":
#     print("Closing client socket now...")
#     server_socket.sendto("Quit.".encode(), client_address)
#     break

# NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# msg = "heee2daw"
# for char in msg:
#     for number in NUMS:
#         if number not in char:
#             print(char + " " + str(number))

# import timeit
#
# start = timeit.timeit()
# x = 2
# p = input("d")
# print(start)
# end = timeit.timeit()
# a = input("d")
# print(end)
# print(end - start)
# import time
#
# start = time.time()
# s = input("wait")
# print(start)
# end = time.time()
# e = input("wait")
# print(end)
# print(end - start)
# from datetime import datetime
# wait = 2
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print(current_time)
# p = int(current_time.split(":")[2])
# start_time = time.time()
# w = input('da')
# print(start_time)
# end_time = time.time()
# wd = input('daaw')
# time_elapsed = (end_time - start_time)
# print(time_elapsed)
# import timeit
#
#
# def func():
#     pass
#
#
# execution_time = timeit.timeit(func, number=1)
#
# print(execution_time)
# import time
# start = time.process_time()
# # your code here
# wada = input("fwe")
# print(time.process_time() - start)
#
# start = time.time()
#
# # your code
# ada = input("awda")
# # end
#
# print(f'Time: {time.time() - start}')
IP_dst = "8.8.8.8"
#
#
# def like6_12(domain):
#     dns_p = IP(dst=IP_dst) / UDP(dport=53) / DNS(qdcount=1) / DNSQR(qname=domain)
#     response_packet = sr1(dns_p, verbose=0)
#     s = response_packet[DNS].summary
#     s = str(s)
#     s = s.split("rdata=")[1]
#     if s.isdigit():
#         print("The domain: ", domain)
#         print("The requested IP: ", s)
#         return s
#     else:
#         s = response_packet[DNS].summary
#         s = str(s)
#         s = s.split("|")[-3]
#         s2 = s.split("rdata=")[1]
#         return s, s2
#
#
# url = input("domain: ")
# print(like6_12(domain=url)[-1])


# def ip_same_check(ip1, ip2):
#     count = 0
#     if ip1.split(".")[0] == ip2.split(".")[0]:
#         count += 1
#     if ip1.split(".")[1] == ip2.split(".")[1]:
#         count += 1
#     if ip1.split(".")[2] == ip2.split(".")[2]:
#         count += 1
#     if ip1.split(".")[3] == ip2.split(".")[3]:
#         count += 1
#     if count >= 3:
#         return True
#     else:
#         return False


# print("The address: " + str(client_address))
# data = client_data.decode()
# print("Client sent: " + data)
# response = "port: " + data
# if data.isdigit():
#     data = int(data)
#     print("The port: " + str(data))


# client_address_port = (SRC_IP, data)
# # server_socket.sendto("".encode(), client_address_port)
# server_socket.sendto(response.encode(), client_address)


# p = (IP(ttl=4, dst='142.250.185.68') / ICMP())
# d = sr1(p, verbose=0)
# d.show()

from scapy.all import scapy


# hostname = "jvns.ca"
# for i in range(1, 28):
#     pkt = IP(dst=hostname, ttl=i) / ICMP()
#     # Send the packet and get a reply
#     reply = sr1(pkt, verbose=0)
#     # reply.show()
#     if reply is None:
#         # No reply =(
#         break
#     elif reply.type == 3:
#         # We've reached our destination
#         print("Done!", reply.src)
#         break
#     else:
#         # We're in the middle somewhere
#         print("%d hops away: " % i, reply.src)
# print("End...")


def like6_12(url):
    """

    :param url:
    :return: the ip of the url.
    """
    dns_p = IP(dst=IP_dst) / UDP(dport=53) / DNS(qdcount=1) / DNSQR(qname=url)
    response_packet = sr1(dns_p, verbose=0)
    s = response_packet[DNS].summary
    s = str(s)
    s = s.split("rdata=")[1]
    if s.isdigit():
        print("The domain: ", url)
        print("The requested IP: ", s)
        return str(s)
    else:
        s = response_packet[DNS].summary
        s = str(s)
        s = s.split("|")[-3]
        s2 = s.split("rdata=")[1]
        return str(s2)


# while r < 700 and l1 < 600 and l2 < 600:
#     screen.fill(WHITE)
#     screen.blit(img, (0, 0))  # (0, 0) --> index of small top corner screen.
#     pygame.display.flip()  # shows the changes!
#     clock.tick(REFRESH_RATE)
#     pygame.draw.line(surface=screen, color=RED, start_pos=[l1, r], end_pos=[l2, r], width=4)
#     pygame.display.flip()
#     r -= 0.5  # the x
#     l1 -= 0.5  # the y of the start
#     l2 += 0.5  # the y of the end
# r = 360
# l1 = 260
# l2 = 460

#
# def gama1(num) -> int:
#     lis = [int(x) for x in str(num)]
#     lis.sort(reverse=True)
#     return lis
#
#
# # print(gama1(num=251))
# def gama2(a, b):
#     mutual_list = [x for x in a if x in b]  # list comprehension
#     print(mutual_list)
#
#
# @gama1
# def tries():
# #     print(";")
#     pass


# print(tries)
#
# ar = [1, 2, 3, 4, 5, 6]
# br = [89, 4, 23, 2, 1, 2]
# print(gama2(ar, br))
#
# with open('data.txt', 'r') as file:
#     data = file.read().replace('\n', '')

# rate = 10
# num_checker = 0
# chars_checker = 0
# dictionary_rate = {
#     'server name': "name.log"
# }
# numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
#          "k", "m", "l", "n", "o", "p", "q", "r", "s", "t",
#          "u", "v", "w", "x", "y", "z"]
# signs = ['?', '!', '|', '<', '>', '@', "#", '$', '%', '^',
#          '&', '*', '(', ')', '-', '_', '+', '=']
# sign_flag = False
# BAD_PASSWORDS = ["password", "qwerty", "abc", "love"]
# rate_list = ["weak", "medium", "strong", "very strong"]
# password = input("Enter Your Password:")
# for p in BAD_PASSWORDS:
#     if p in password:
#         rate = 0
# password_length = len(password)
# if password_length < 4:
#     rate = 0
# elif 4 < password_length < 8:
#     rate = 5
# else:
#     print("checks char...")
# for char in password:
#     if char in numbers:
#         num_checker += 1
#     elif char in chars:
#         chars_checker += 1
#     elif char in signs:
#         sign_flag = True
# if num_checker == password_length:
#     rate = 0
# elif chars_checker == password_length:
#     rate = 3
# elif num_checker + chars_checker == password_length:
#     rate = 5
# elif num_checker + chars_checker != password_length and\
#      sign_flag and num_checker > 0 and chars_checker > 0:
#     rate = 7
# else:
#     print("checks rate...")
# if rate > 8:
#     print(rate_list[-1])
# elif rate > 6:
#     print(rate_list[-2])
# elif rate > 4:
#     print(rate_list[-3])
# elif rate > 0:
#     print(rate_list[-4])
#
ar = [1, 2, 3, 4, 5, 6]
n = map(lambda x: x * x, ar)
# print(n)
li = [x for x in range(1, 2) if x % 2]
# print(li)

import requests

data = requests.get("https://www.google.com")
print(data.headers)
# print(data.cookies)
file_ob = open("C:\\Cyber\\From.txt", 'w')
file_ob.write(str(data.headers))
file_ob.close()
import random

c = random.choice(ar)

