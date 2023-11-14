import io
from PIL import Image
from scapy.layers.inet import IP, ICMP, TCP
from scapy.packet import Raw
from scapy.sendrecv import sniff, send

# SRC_IP = "192.168.1.32"
DST_IP = "192.168.56.1"
FOLDER = "C:\Cyber"


def show_photo(photo_bytes):
    """
    :param photo_bytes:
    shows the photo.
    """
    photo = Image.open(io.BytesIO(photo_bytes))
    photo.show()


def save_photo(folder_path, photo_bytes):
    """
    :param folder_path:
    :param photo_bytes:
    take the photo of the screenshot and save it in a known location.
    """
    photo = Image.open(io.BytesIO(photo_bytes))
    photo.save(folder_path + r"\photo27.jpg")


def filters(pack):
    """
    :param pack:
    :return: True or False if the request is relevant.
    """
    return ICMP in pack and IP in pack and TCP in pack and pack[IP].src == DST_IP


def main():
    data = None
    while data is None:
        data = sniff(lfilter=filters, count=1, timeout=5)
        if data is not None:
            if data[Raw].load is not None:
                file_data = data[Raw].load
                show_photo(file_data)
                save_photo(FOLDER, file_data)
                for i in range(1, 5):
                    send(IP(dst=DST_IP) / ICMP(type="echo-request") / Raw(load="OK"))
        else:
            break


if __name__ == '__main__':
    main()
print("disconnecting..")
