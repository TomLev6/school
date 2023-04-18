import datetime
import pyodbc
# import logging
from datetime import datetime


class Odbc:
    # logging.basicConfig(filename='db_sql.log', filemode='w', level=logging.INFO)
    # logging.warning('This will get logged to a file')

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

    # @staticmethod
    def connect_and_close(func):  #
        def wrapper(self, *args, **kwargs):
            """
            :type self: Odbc
            """
            self.__connect()
            val = func(self, *args, **kwargs)
            self.__close_connection()
            return val
        return wrapper

    def __connect(self):
        self.conn = pyodbc.connect(self.conn_string)
        # Create a cursor
        self.cursor = self.conn.cursor()

    @connect_and_close
    def insert_new_user(self, ip: str, packets: int, time: str):
        # Insert data into the table
        self.cursor.execute("INSERT INTO Users (userIP, PacketsAmount, StartTime) VALUES (?, ?, ?)",
                            (ip, packets, time))
        # Commit changes
        self.conn.commit()
        ###########print("Commit changes.. ,inserting", (ip, packets, time))

    @connect_and_close
    def insert_to_blacklist(self, ip: str, mode: str, starttime: datetime):
        self.cursor.execute("INSERT INTO BlackList (userIP, mode, StartDate) VALUES (?, ?, ?)",
                            (ip, mode, starttime))
        # Commit changes
        self.conn.commit()
        ###########print("Commit changes..")

    @connect_and_close
    def insert_to_whitelist(self, ip: str, mode: str, starttime: datetime):
        self.cursor.execute("INSERT INTO Whitelist (userIP, mode, StartDate) VALUES (?, ?, ?)",
                            (ip, mode, starttime))
        # Commit changes
        self.conn.commit()

    def __close_connection(self):
        # Close connection
        self.conn.close()
        ###########print("closing connection...")

    @connect_and_close
    def find_in_users(self, ip: str):
        ###########print(ip, "[SEARCHING-Users]")
        self.cursor.execute(f"SELECT * FROM Users WHERE userIP ='{ip}';")
        result = self.cursor.fetchall()
        if len(result) > 0:
            ###########print("user already in Users!")
            return True
        return False

    @connect_and_close
    def find_in_blacklist(self, ip: str):
        ###########print(ip, "[SEARCHING-Blacklist]")
        self.cursor.execute(f"SELECT * FROM BlackList WHERE userIp ='{ip}';")
        result = self.cursor.fetchall()
        if len(result) > 0:
            ###########print("user already in the Blacklist!")
            return True
        return False

    @connect_and_close
    def find_in_whitelist(self, ip: str):
        ###########print(ip, "[SEARCHING-Blacklist]")
        self.cursor.execute(f"SELECT * FROM WhiteList WHERE userIp ='{ip}';")
        result = self.cursor.fetchall()
        if len(result) > 0:
            ###########print("user already in the Blacklist!")
            return True
        return False

    @connect_and_close
    def update_user_data(self, ip: str, packets: int):
        self.cursor.execute("UPDATE Users SET userIP = ?, PacketsAmount = ?",
                            (ip, packets))
        self.conn.commit()

    @connect_and_close
    def get_user_packets(self, ip: str):
        self.cursor.execute(f"SELECT * FROM Users WHERE userIp ='{ip}';")
        result = self.cursor.fetchall()
        if len(result) > 0:
            res = str(result[0])
            return int(res.split(",")[1])
        else:
            return 0

    @connect_and_close
    def get_user_time(self, ip: str):
        self.cursor.execute(f"SELECT * FROM Users WHERE userIp ='{ip}';")
        res = str(self.cursor.fetchall()).split(",")[2]
        return res.split("'")[1]

    @connect_and_close
    def delete_user(self, ip: str, db: str):
        self.cursor.execute(f"DELETE From {db} WHERE userIP ='{ip}';")
        # Commit changes
        self.conn.commit()

    @connect_and_close
    def clear_db(self, db: str):
        self.cursor.execute(f"DELETE From {db};")
        # Commit changes
        self.conn.commit()



o = Odbc()
o.clear_db('Users')
o.clear_db('Blacklist')
# o.close_connection()
# o.insert_new_user("100.111.111.111", 55, str(datetime.now()))
# o.update_user_data("100.111.111.111", 90)
#print(o.get_user_time("100.111.111.111"))
# o.find_in_users("100.111.111.111")  # , 55, str(datetime.now())
# o.delete_user("100.111.111.111", "Users")
