import socket

PORT = 55555
MAX_PACKET = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
full_msg = []
server_socket.bind(("0.0.0.0", PORT))
while "$" not in full_msg:
    (client_data, client_address) = server_socket.recvfrom(MAX_PACKET)
    data = client_data.decode()
    len_msg_part = int(data)
    print("received:", data)
    while len_msg_part != 0:
        len_msg_part -= 1
        (client_data, client_address) = server_socket.recvfrom(MAX_PACKET)
        data = client_data.decode()
        full_msg.append(data)
        print("received:", data)

print("the full massage:", full_msg.remove("$"))
server_socket.close()
