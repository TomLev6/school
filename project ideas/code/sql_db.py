import datetime

import pyodbc


class Odbc:
    def __init__(self):
        pass
        # Connect to the database
        self.DRIVER_NAME = 'SQL SERVER'
        self.SERVER_NAME = "DESKTOP-4K52IRC"
        self.DATABASE_NAME = 'SQLTutorial'
        self.cursor = None
        self.conn = None
        # uid=<username>;
        # pwd=<password>;
        self.conn_string = f"""DRIVER={{{self.DRIVER_NAME}}};
        SERVER={self.SERVER_NAME};DATABASE={self.DATABASE_NAME};
        Trust_Connection=yes;"""

    def connect(self):
        self.conn = pyodbc.connect(self.conn_string)
        # Create a cursor
        self.cursor = self.conn.cursor()

    def insert_new_user(self, ip: str, packets: int, time: str):
        # Insert data into the table
        self.cursor.execute("INSERT INTO Users (userIP, PacketsAmount, StartTime) VALUES (?, ?, ?)",
                            (ip, packets, time))
        # Commit changes
        self.conn.commit()
        print("Commit changes..")

    def insert_to_blacklist(self, ip: str, mode: str, starttime: datetime):
        self.cursor.execute("INSERT INTO BlackList (userIP, mode, StartDate) VALUES (?, ?, ?)",
                            (ip, mode, starttime))
        # Commit changes
        self.conn.commit()
        print("Commit changes..")

    def close_connection(self):
        # Close connection
        self.conn.close()

    def find_in_users(self, ip: str):
        self.cursor.execute(f"SELECT * FROM Users WHERE userIp ='{ip}';")
        result = self.cursor.fetchall()
        if len(result) == 0:
            return True
        else:
            print("user already in users!")
            return False

    def find_in_blacklist(self, ip: str):
        self.cursor.execute(f"SELECT * FROM BlackList WHERE userIp ='{ip}';")
        result = self.cursor.fetchall()
        if len(result) == 1:
            return True
        return False

    def update_user_data(self, ip: str, packets: int):
        self.cursor.execute("UPDATE Users SET userIP = ?, PacketsAmount = ?",
                            (ip, packets))
        self.conn.commit()
        print("Commit changes..")

    def get_user_packets(self, ip: str):
        self.cursor.execute(f"SELECT * FROM Users WHERE userIp ='{ip}';")
        res = str(self.cursor.fetchall())
        if len(res) != 0:
            return int(str(self.cursor.fetchall()).split(",")[1])

    def get_user_time(self, ip: str):
        self.cursor.execute(f"SELECT * FROM Users WHERE userIp ='{ip}';")
        res = str(self.cursor.fetchall()).split(",")[2]
        return res.split("'")[1]

    def delete_user(self, ip: str, db: str):
        self.cursor.execute(f"DELETE From {db} WHERE userIP ='{ip}';")
        # Commit changes
        self.conn.commit()
        print("Commit changes..")


o = Odbc()
o.connect()
# o.insert_new_user("100.111.111.111", 55, "2.3333")
# o.update_user_data("100.111.111.111", 90)
# print(o.get_user_time("100.111.111.111"))
# o.find_in_users("100.111.111.111", 55, "2.3333")
# o.delete_user("100.111.111.111", "Users")
