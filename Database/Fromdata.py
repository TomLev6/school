from database import Database

FILE_LOCATION = "databasef.txt"


def main():
    dictionary = {
        "name": "Tom"
    }
    d = Database(dictionary)
    print(d)
    d.set_value("name", "yon")
    print(d)


if __name__ == '__main__':
    main()
