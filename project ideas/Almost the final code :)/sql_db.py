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
        # uid=<username>;
        # pwd=<password>;
        self.conn_string = f"""DRIVER={{{self.DRIVER_NAME}}};
        SERVER={self.SERVER_NAME};DATABASE={self.DATABASE_NAME};
        Trust_Connection=yes;"""

    def __connect(self):
        conn = pyodbc.connect(self.conn_string)
        # Create a cursor
        return conn, conn.cursor()

    def insert_new_user(self, ip: str, starttime: datetime):
        conn, cursor = self.__connect()
        # Insert data into the table
        cursor.execute("INSERT INTO Users (userIP, startdate) VALUES (?, ?)",
                       (ip, starttime))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_blacklist(self, ip: str, starttime: datetime):
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO BlackList (userIP, startdate) VALUES (?, ?)",
                       (ip, starttime))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_whitelist(self, ip: str, starttime: datetime):
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO Whitelist (userIP, startdate) VALUES (?, ?)",
                       (ip, starttime))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_AllRequests(self, ip: str, starttime: datetime, packetssent: int):
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO AllRequests (userIP, startdate, packetssent) VALUES (?, ?, ?)",
                       (ip, starttime, packetssent))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_ServerRequests(self, ip: str, starttime: datetime, packetssent: int):
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO ServerRequests (userIP, startdate, packetssent) VALUES (?, ?, ?)",
                       (ip, starttime, packetssent))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def find_in_Requests(self, ip: str, table: str):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM {table} WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def find_in_users(self, ip: str):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM Users WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def find_in_blacklist(self, ip: str):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM BlackList WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def find_in_whitelist(self, ip: str):
        conn, cursor = self.__connect()
        # cursor.execute(f"SELECT * FROM WhiteList WHERE userIP ='{ip}';")
        cursor.execute(f"SELECT userIP FROM WhiteList WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def users_check(self):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM Users;")
        users_list = cursor.fetchall()
        for user in users_list:
            if not self.find_in_whitelist(user[0]):  # user not in Whitelist_users:
                self.insert_to_blacklist(user[0], datetime.now())
            self.delete_user(user[0], "Users")
        conn.commit()
        cursor.close()
        conn.close()

    def total_request_count(self):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM AllRequests;")
        requests_list = cursor.fetchall()
        # self.clear_db("AllRequests")
        cursor.close()
        conn.close()
        return requests_list

    def server_request_count(self):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM ServerRequests;")
        requests_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests_list

    def delete_user(self, ip: str, db: str):
        conn, cursor = self.__connect()
        cursor.execute(f"DELETE From {db} WHERE userIP ='{ip}';")
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def clear_db(self, db: str):
        conn, cursor = self.__connect()
        cursor.execute(f"DELETE From {db};")
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def get_packets_amount(self, ip: str, table: str):
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM {table} WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        if len(result) != 0:
            result = str(result).split(",")[-1]
            result = str(result).split(")")[0]
            return int(result)
        return 0

    def add_packet(self, ip: str, table: str):
        conn, cursor = self.__connect()
        packets = self.get_packets_amount(ip, table) + 1
        cursor.execute(f"UPDATE {table} SET packetssent = {packets} WHERE userIP ='{ip}';")
        conn.commit()
        cursor.close()
        conn.close()

#
# o = Odbc()
# o.insert_to_ServerRequests("100.0.0.0", datetime.now(), 1)
# print(str(o.get_packets_amount("100.0.0.0", "ServerRequests")))
# o.add_packet("100.0.0.0", "ServerRequests")
# print(str(o.get_packets_amount("100.0.0.0", "ServerRequests")))
# o.clear_db("ServerRequests")
# o.users_check()
# o.update_user_data("100.111.111.111", 90)
# print(o.get_user_time("100.111.111.111"))
# o.find_in_users("100.111.111.111")  # , 55, str(datetime.now())
# o.delete_user("100.111.111.111", "Users")
