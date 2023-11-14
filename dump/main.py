"""
Author: Tom Lev
Program name: main.py
Description: Encrypt data and decrypt encrypted data.
Date: 2.10.21
"""
import sys

KEY_DICTIONARY = {
    "Y": "10",
    "Z": "11",
    "a": "12",
    "b": "13",
    "c": "14",
    "d": "15",
    "e": "16",
    "f": "17",
    "g": "18",
    "h": "19",
    "i": "30",
    "j": "31",
    "k": "32",
    "l": "33",
    "m": "34",
    "n": "35",
    "o": "36",
    "p": "37",
    "q": "38",
    "r": "39",
    "E": "40",
    "F": "41",
    "G": "42",
    "H": "43",
    "I": "44",
    "J": "45",
    "K": "46",
    "L": "47",
    "M": "48",
    "N": "49",
    "A": "56",
    "B": "57",
    "C": "58",
    "D": "59",
    "O": "60",
    "P": "61",
    "Q": "62",
    "R": "63",
    "S": "64",
    "T": "65",
    "U": "66",
    "V": "67",
    "W": "68",
    "X": "69",
    "s": "90",
    "t": "91",
    "u": "92",
    "v": "93",
    "w": "94",
    "x": "95",
    "y": "96",
    "z": "97",
    " ": "98",
    ",": "99",
    '.': "100",
    "'": "101",
    "!": "102",
    "-": "103",
}
REVERSED_DICTIONARY = {
    "10":"Y",
    "11":"Z",
    "12":"a",
    "13":"b",
    "14":"c",
    "15":"d",
    "16":"e",
    "17":"f",
    "18":"g",
    "19":"h",
    "30":"i",
    "31":"j",
    "32":"k",
    "33":"l",
    "34":"m",
    "35":"n",
    "36":"o",
    "37":"p",
    "38":"q",
    "39":"r",
    "40":"E",
    "41":"F",
    "42":"G",
    "43":"H",
    "44":"I",
    "45":"J",
    "46":"K",
    "47":"L",
    "48":"M",
    "49":"N",
    "56":"A",
    "57":"B",
    "58":"C",
    "59":"D",
    "60":"O",
    "61":"P",
    "62":"Q",
    "63":"R",
    "64":"S",
    "65":"T",
    "66":"U",
    "67":"V",
    "68":"W",
    "69":"X",
    "90":"s",
    "91": "t",
    "92": "u",
    "93": "v",
    "94": "w",
    "95": "x",
    "96": "y",
    "97": "z",
    "98": " ",
    "99":",",
    "100":".",
    "101":"'",
    "102":"!",
    "103":"-",
}


def asserts():
    """
    בודק אם אפשר להצפין ולפענך.
    :return: True or False
    """
    data = ""
    for item in KEY_DICTIONARY:
        data += item
    encrypt(data, '2.txt')
    encrypted_msg = "10,11,12,13,14,15,16,17,18,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,56," \
                    "57,58,59,60,61,62,63,64,65,66,67,68,69,90,91,92,93,94,95,96,97,98,99,100,101,102,103"
    if encrypted_msg != readfile('2.txt'):
        return False
    msg = decrypt(encrypted_msg, False)
    if msg != data:
        return False
    return True


def readfile(filename):
    """
    read from a file
    :return: the info
    """
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        file = open(filename, 'w')
        file.close()
        file = open(filename, 'r')
    filedata = file.read()
    file.close()
    return filedata


def writefile(filename, filedata):
    """
    write in the file
    """
    file = open(filename, 'w')
    file.write(filedata)
    file.close()


def encrypt(data, filename='1.txt'):
    """
    encrypt the message to the file
    :return: the encrypted message
    """
    encrypted_data = ""
    for char in data:
        if char in KEY_DICTIONARY:
            encrypted_data += KEY_DICTIONARY[char] + ","
    encrypted_data = encrypted_data[:-1]
    writefile(filename, encrypted_data)


def decrypt(encrypted, print_or_return=True):
    """
    decrypt the message to the file
    :return: the decrypted message
    """
    encrypted_list = encrypted.split(",")
    data = ""
    for char in encrypted_list:
        if char in REVERSED_DICTIONARY:
            data += REVERSED_DICTIONARY[char]
    if print_or_return:
        print("the decrypted msg: " + data)
    else:
        return data


if __name__ == '__main__':
    assert asserts()
    if sys.argv[1] == "encrypt":
        encrypt(input("enter something to encrypt: "))
    elif sys.argv[1] == "decrypt":
        decrypt(readfile('1.txt'))
    else:
        print("I don't get it!, run the program again! ")
