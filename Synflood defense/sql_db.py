"""
Author: Tom Lev
Date: 11/05/23
"""
import datetime
import pyodbc
from datetime import datetime


class Odbc:

    def __init__(self):
        """
        the init function, which initializes all the parameters.
        creates the connection string which later we using to connect to the database.
        """
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
        """
        connecting to the database.
        :returns: conn => connection /open -> / close
                  conn.cursor => cursor -> all the actions on the database/
        """
        conn = pyodbc.connect(self.conn_string)
        # Create a cursor
        return conn, conn.cursor()

    def insert_new_user(self, ip: str, starttime: datetime):
        """
        inserts the received ip, starttime to the Users table.
        :param ip: str
        :param starttime: datetime
        :return: nothing
        """
        conn, cursor = self.__connect()
        # Insert data into the table
        cursor.execute("INSERT INTO Users (userIP, startdate) VALUES (?, ?)",
                       (ip, starttime))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_blacklist(self, ip: str, starttime: datetime):
        """
        inserts the received ip, starttime to the BlackList table.
        :param ip: str
        :param starttime: datetime
        :return: nothing
        """
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO BlackList (userIP, startdate) VALUES (?, ?)",
                       (ip, starttime))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_whitelist(self, ip: str, starttime: datetime):
        """
        inserts the received ip, starttime to the WhiteList table.
        :param ip: str
        :param starttime: datetime
        :return: nothing
        """
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO WhiteList (userIP, startdate) VALUES (?, ?)",
                       (ip, starttime))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_AllRequests(self, ip: str, starttime: datetime, packetssent: int):
        """
        inserts the received ip, starttime, packetssent to the AllRequests table.
        :param ip: str
        :param starttime: datetime
        :param packetssent: int
        :return: nothing
        """
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO AllRequests (userIP, startdate, packetssent) VALUES (?, ?, ?)",
                       (ip, starttime, packetssent))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def insert_to_ServerRequests(self, ip: str, starttime: datetime, packetssent: int):
        """
        inserts the received ip, starttime, packetssent to the ServerRequests table.
        :param ip: str
        :param starttime: datetime
        :param packetssent: int
        :return: nothing
        """
        conn, cursor = self.__connect()
        cursor.execute("INSERT INTO ServerRequests (userIP, startdate, packetssent) VALUES (?, ?, ?)",
                       (ip, starttime, packetssent))
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def find_in_Requests(self, ip: str, table: str):
        """
        :returns True if the received ip (userIP) in the received table, else False.
        :param ip: str
        :param table:str
        :return: bool
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM {table} WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def find_in_users(self, ip: str):
        """
        :returns True if the received ip (userIP) in the Users table, else False.
        :param ip: str
        :return: bool
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM Users WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def find_in_blacklist(self, ip: str):
        """
        :returns True if the received ip (userIP) in the Blacklist table, else False.
        :param ip: str
        :return: bool
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT * FROM BlackList WHERE userIP ='{ip}';")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            return True
        return False

    def find_in_whitelist(self, ip: str):
        """
        :returns True if the received ip (userIP) in the WhiteList table, else False.
        :param ip: str
        :return: bool
        """
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
        """
        checks if the user ip in the Users table in the Whitelist table then deletes him from the Users table,
        else blocking the ip because if he didn't connect in order to make the three way hand shake with the server
        it is an attack!
        :return: nothing
        """
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
        """
        gets all the users ip (userIP) from the AllRequests table.
        :return: list[Row]
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM AllRequests;")
        requests_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests_list

    def server_request_count(self):
        """
        gets all the users ip (userIP) from the ServerRequests table.
        :return: list[Row]
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM ServerRequests;")
        requests_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests_list

    def server_users_count(self, table: str):
        """
        returns all the users ip amount (userIP) from the received table.
        :return: int
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM {table};")
        requests_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return len(requests_list)

    def delete_user(self, ip: str, db: str):
        """
        delets user in the received table with the received ip.
        :param ip:
        :param db:
        :return: nothing
        """
        conn, cursor = self.__connect()
        cursor.execute(f"DELETE From {db} WHERE userIP ='{ip}';")
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def clear_db(self, db: str):
        """
        clears all the table values.
        :param db:
        :return: nothing
        """
        conn, cursor = self.__connect()
        cursor.execute(f"DELETE From {db};")
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

    def get_packets_amount(self, ip: str, table: str):
        """
        gets the packet amount (the packetssent value) from the received ip and table.
        :param ip:
        :param table:
        :return: int
        """
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

    def get_startdate(self, table: str):
        """
        gets a table parameter and returns the data of the last user who joined the received table.
        :param table: str
        :return: str
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT startdate FROM {table};")
        result = cursor.fetchall()
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        if len(result) != 0:
            date = str(result).split(")")[-3]
            date = date.split("(")[-1]
            date = date.replace(", ", ":")
            return date
        return None

    def get_all_users(self, table):
        """
        received a table name and returns a list of all the ips in the table.
        :param table: str
        :return: List[Row]
        """
        conn, cursor = self.__connect()
        cursor.execute(f"SELECT userIP FROM {table};")
        result = cursor.fetchall()
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def add_packet(self, ip: str, table: str):
        """
        adds one packet to his ip in the table that the function gets for every packet the server received.
        :param ip: str
        :param table: str
        :return: nothing
        """
        conn, cursor = self.__connect()
        packets = self.get_packets_amount(ip, table) + 1
        cursor.execute(f"UPDATE {table} SET packetssent = {packets} WHERE userIP ='{ip}';")
        conn.commit()
        cursor.close()
        conn.close()
