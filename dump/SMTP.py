import socket

"""
Author: Tom Lev
A client on smtp protocol.
Communicate with smtp server.
"""
IP = "54.71.128.194"
PORT = 587
PASSWORD = "1234"
FINISH = "@gmx.com"
SUBJECT = "Subject: Let's have party or something"
MESSAGE = "Today at my home It's going to be fun, don't forget to bring some food and beers.\r\n" \
          " Yours, Frusta.\r\n."
MAX_PACKET = 1024
TO = "bads"
NAME = "Tom"
RES = '250-mail.gmx.com GMX Mailservices\r\n' \
      '250-8BITMIME\r\n' \
      '250-ENHANCEDSTATUSCODES\r\n' \
      '250-SIZE250-AUTH=LOGIN PLAIN\r\n' \
      '250-AUTH LOGIN PLAIN\r\n' \
      '250 STARTTLS\r\n'
TO_FINISH = '@'+TO+'.com'
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    my_socket.connect((IP, PORT))
    print("the server connected....")
    res = my_socket.recv(MAX_PACKET).decode()
    if "220 mail.gmx.com GMX Mailservices ESMTP" in res and '\r\n' in res:  # לא בטוח אם זה חלק מהבקשה..
        my_socket.send("EHLO\r\n".encode())
        res3 = my_socket.recv(MAX_PACKET).decode()
        if '250' in res3:
            my_socket.send("AUTH PLAIN AGZydXN0YUBnbXguY29tAFBhc3N3b3JkMSE=\r\n".encode())
            res4 = my_socket.recv(MAX_PACKET).decode()
            if res4.split(" ")[2:4] == "Go ahead":
                from_name = NAME + FINISH
                my_socket.send(f"MAIL FROM:<{from_name}>".encode())
                res5 = my_socket.recv(MAX_PACKET).decode()
                if res5.split(" ")[2] == "ok":
                    to_name = TO_FINISH
                    my_socket.send(f"RCPT TO:{to_name}".encode())
                    res6 = my_socket.recv(MAX_PACKET).decode()
                    if res6.split(" ")[2] == "ok":
                        data = "DATA" + '\x00' + from_name + FINISH + '\x00' + PASSWORD
                        my_socket.send(data.encode())
                        res7 = my_socket.recv(MAX_PACKET).decode()
                        if res7.split(" ")[2:4] == "Go ahead":
                            my_socket.send(f"{SUBJECT}\r\n\r\n{MESSAGE}".encode())
                            res8 = my_socket.recv(MAX_PACKET).decode()
                            if res8.split(" ")[2:4] == "Message accepted":
                                my_socket.send("QUIT".encode())
except socket.error as err:
    print("there is a problem: " + str(err))
finally:
    my_socket.close()
