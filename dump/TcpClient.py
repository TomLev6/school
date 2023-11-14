import socket

PORT = 8820
IP = "127.0.0.1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((IP, PORT))
    while True:
        msg = input("enter msg: ")
        client.send(msg.encode())
        print(client.recv(1024).decode())
        if msg == "Quit":
            break
except socket.error as e:
    print(str(e))
finally:
    client.close()
