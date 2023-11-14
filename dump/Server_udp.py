import socket

PORT = 8821
MAX_PACKET = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("0.0.0.0", PORT))
while True:
    (client_name, client_address) = server_socket.recvfrom(MAX_PACKET)
    data = client_name.decode()
    response = "Hello " + data
    server_socket.sendto(response.encode(), client_address)
    server_socket.close()
