import socket
import threading

IP = '0.0.0.0'
PORT = 8820
print_lock = threading.Lock()
MAX = 1024
ENCRYPTED_MSG = "5e8667a439c68f5145dd2fcbecf02209"  # 87654321
LEN = 8
OPTIONS = 10 ** LEN

start = 0
clients = 4
end = OPTIONS / 40
plus = 1
found = False


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
    creates threads for any client that connects to the server,
     and send him to the handle_client def.
    :return: None
    """
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    global found
    while True:
        try:
            while not found:
                client_socket, client_address = server_socket.accept()
                print("Client connected")
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                thread.start()
            if found:
                break
            break
        except socket.error as err:
            print(str(err))
        finally:
            server_socket.close()


def handle_client(client_socket):
    """
    handles the current client
    :param client_socket: socket
    :return: None
    """
    global found
    try:
        while True:
            while not found:
                msg = client_socket.recv(MAX).decode()
                if msg == "ready":
                    r = give_range()
                    client_socket.send(r.encode())
                    data = str(client_socket.recv(MAX))
                    data = data.split("'")[1]
                    if data != '0':
                        print("the decrypted message: ", data)
                        found = True
                break
    except socket as er:
        print(str(er))
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
