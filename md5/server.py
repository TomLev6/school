import socket
import threading

IP = '0.0.0.0'
PORT = 8820
print_lock = threading.Lock()
MAX = 1024

LEN = 8
start = 0
plus = 1
clients = 4
OPTIONS = 10 ** LEN
end = OPTIONS / clients
ENCRYPTED_MSG = "5e8667a439c68f5145dd2fcbecf02209"  # 87654321


def give_range():
    global start
    global end
    global plus
    msg = str(start) + "|" + str(end) + "|" + ENCRYPTED_MSG
    if start < plus:
        plus = end
    start = end
    end += plus
    return msg


def main():
    """
    :return:
    """
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print("Client connected")
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            # thread.join()
    except socket.error as er:
        print(str(er))
    finally:
        server_socket.close()


def handle_client(client_socket):
    """
    handles the current client
    :param client_socket: socket
    :return:
    """
    msg = client_socket.recv(MAX).decode()
    if msg == "ready":
        r = give_range()
        print(r)
        client_socket.send(r.encode())
        ans = client_socket.recv(MAX)
        if ans != b'0':
            ans = ans.decode()
            print("the decrypted message: ", ans)
    client_socket.close()


if __name__ == '__main__':
    main()
