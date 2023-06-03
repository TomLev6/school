"""
Author: Tom Lev
Date: 11/05/23
"""
import threading
import tkinter as tk
import multiprocessing
from tkinter import messagebox


class Tk:
    def __init__(self, window: tk.Tk, main_function, unblocking_function, db):
        """
        the init function, which initializes all the parameters.
        :param window: tk.Tk
        :param main_function: function
        :param unblocking_function: function
        :param db: database
        """
        self.main_function_process = None
        self.unblocking_function_process = None
        self.window = window
        self.main_function = main_function
        self.unblocking_function = unblocking_function
        self.window.title("Firewall Application")
        self.background_image = tk.PhotoImage(file="backgr.png")
        self.db = db
        self.largefont = ("Cascadia Code", 25)
        self.is_on = False
        self.unblocking = False
        self.port = "8909"
        self.ip = "172.16.6.69"
        self.max_pc_packets = 24000
        self.max_server_packets = 10000
        self.whitelist_len_data = 0
        self.blacklist_len_data = 0
        self.server_len_data = 0
        self.pc_len_data = 0
        self.B = "BlackList"
        self.S = "ServerRequests"
        self.A = "AllRequests"
        self.W = "WhiteList"
        self.whitelist_last_data = None
        self.blacklist_last_data = None
        self.server_last_data = None
        self.pc_last_data = None
        self.log_text = None

        # labels
        self.label = tk.Label(self.window, text="Welcome to the Firewall Application", font=self.largefont)
        self.background_label = tk.Label(self.window, image=self.background_image)

        # menu frame
        self.setting_label = tk.Label(self.window, text="Settings", font=self.largefont)
        self.whitelist_label = tk.Label(self.window, text="White List", font=self.largefont)
        self.blacklist_label = tk.Label(self.window, text="Black List", font=self.largefont)
        self.server_packets_label = tk.Label(self.window, text="Server Packets", font=self.largefont)
        self.all_packets_label = tk.Label(self.window, text="All Packets", font=self.largefont)

        # settings or options frame
        self.server_port_label = tk.Label(self.window, text="Server Port:", font=self.largefont)
        self.server_ip_label = tk.Label(self.window, text="Server IP:", font=self.largefont)
        self.max_packets_rate_pc_label = tk.Label(self.window, text="Max Packets Rate PC:", font=self.largefont)
        self.max_packets_rate_server_label = tk.Label(self.window, text="Max Packets Rate Server:", font=self.largefont)
        self.allow_unblocking_label = tk.Label(self.window, text="Allow Unblocking:", font=self.largefont)

        # whitelist frame
        self.whitelist_last_packet_label = tk.Label(self.window, text=f"Last New User\n {self.whitelist_last_data}",
                                                    font=self.largefont)

        self.whitelist_users_count_label = tk.Label(self.window, text=f"Total Users:\n {self.whitelist_len_data}",
                                                    font=self.largefont)

        self.whitelist_ips_listbox = tk.Listbox(self.window, font=self.largefont, fg="green", height=7,
                                                selectmode="browse", width=17)

        # blacklist frame
        self.blacklist_last_packet_label = tk.Label(self.window,
                                                    text=f"Last New Blocked User:\n {self.blacklist_last_data}",
                                                    font=self.largefont)
        self.blacklist_users_count_label = tk.Label(self.window,
                                                    text=f"Total Blocked Users:\n {self.blacklist_len_data}",
                                                    font=self.largefont)
        self.blacklist_ips_listbox = tk.Listbox(self.window, font=self.largefont, fg="green", height=7,
                                                selectmode="browse", width=17)

        # server packets frame
        self.server_users_packets_count_label = tk.Label(self.window,
                                                         text=f"Total Server Requests:\n {self.server_len_data}",
                                                         font=self.largefont)
        self.server_last_packet_label = tk.Label(self.window, text=f"Last New Request:\n {self.server_last_data}",
                                                 font=self.largefont)
        self.server_ips_listbox = tk.Listbox(self.window, font=self.largefont, fg="green", height=7,
                                             selectmode="browse", width=17)

        # all packets frame
        self.pc_users_count_label = tk.Label(self.window, text=f"Total PC Requests:\n {self.pc_len_data}",
                                             font=self.largefont)
        self.pc_last_packet_label = tk.Label(self.window, text=f"Last New Request:\n {self.pc_last_data}",
                                             font=self.largefont)
        self.pc_ips_listbox = tk.Listbox(self.window, font=self.largefont, fg="green", height=7,
                                         selectmode="browse", width=17)

        # buttons
        self.refresh_log_btn = tk.Button(master=self.window, text="Refresh", width=10, height=2,
                                         font=self.largefont, command=self.update_log)
        self.log_data_btn = tk.Button(master=self.window, text="Logging Data", width=14, height=2,
                                      font=self.largefont, command=self.log_command)

        self.run_btn = tk.Button(master=self.window, text="Off", width=10, height=3, font=self.largefont,
                                 command=self.run_on_off, activebackground="green")
        self.unblocking_btn = tk.Button(master=self.window, text="Off", width=10, font=self.largefont,
                                        command=self.allow_unblocking, activebackground="green")

        self.back_to_menu_settings_btn = tk.Button(master=self.window, text="Back", width=10, height=3,
                                                   font=self.largefont, command=self.back_btn_from_settings,
                                                   activebackground="green")
        self.back_to_menu_whitelist_btn = tk.Button(master=self.window, text="Back", width=10, height=3,
                                                    font=self.largefont, command=self.back_btn_from_whitelist,
                                                    activebackground="green")
        self.back_to_menu_blacklist_btn = tk.Button(master=self.window, text="Back", width=10, height=3,
                                                    font=self.largefont, command=self.back_btn_from_blacklist,
                                                    activebackground="green")
        self.back_to_menu_server_packets_btn = tk.Button(master=self.window, text="Back", width=10, height=3,
                                                         font=self.largefont, command=self.back_btn_from_server_packets,
                                                         activebackground="green")
        self.back_to_menu_all_packets_btn = tk.Button(master=self.window, text="Back", width=10, height=3,
                                                      font=self.largefont, command=self.back_btn_from_all_packets,
                                                      activebackground="green")
        self.back_to_menu_log_btn = tk.Button(master=self.window, text="Back", width=10, height=3,
                                              font=self.largefont, command=self.back_btn_from_log,
                                              activebackground="green")

        self.save_server_port_btn = tk.Button(master=self.window, text=" > ", font=self.largefont, width=3,
                                              command=self.save_server_port)
        self.save_server_ip_btn = tk.Button(master=self.window, text=" > ", font=self.largefont, width=3,
                                            command=self.save_server_ip)
        self.save_pc_packets_rate_btn = tk.Button(master=self.window, text=" > ", font=self.largefont, width=3,
                                                  command=self.save_pc_packets_rate)
        self.save_server_packets_rate_btn = tk.Button(master=self.window, text=" > ", font=self.largefont, width=3,
                                                      command=self.save_server_packets_rate)

        # entries
        self.server_port_entry = tk.Entry(master=self.window, font=self.largefont, bd=3, fg="green", width=8)
        self.server_ip_entry = tk.Entry(master=self.window, font=self.largefont, bd=3, fg="green", width=8)
        self.pc_packets_rate_entry = tk.Entry(master=self.window, font=self.largefont, bd=3, fg="green", width=16)
        self.server_packets_rate_entry = tk.Entry(master=self.window, font=self.largefont, bd=3, fg="green", width=20)

        # menubutton
        self.menu_options_btn = tk.Menubutton(master=self.window, text="Options", relief="raised", font=self.largefont)
        self.menu_options_btn.menu = tk.Menu(self.menu_options_btn, tearoff=0)
        self.menu_options_btn["menu"] = self.menu_options_btn.menu
        self.menu_options_btn.menu.add_command(label="Settings", command=self.settings_command, font=self.largefont)
        self.menu_options_btn.menu.add_command(label=self.W, command=self.whitelist_command, font=self.largefont)
        self.menu_options_btn.menu.add_command(label=self.B, command=self.blacklist_command, font=self.largefont)
        self.menu_options_btn.menu.add_command(label=self.S, command=self.server_packets_command,
                                               font=self.largefont)
        self.menu_options_btn.menu.add_command(label=self.A, command=self.all_packets_command,
                                               font=self.largefont)
        self.menu_screen()

    def update_log(self):
        """
        updates the log data, converts the file data into text.
        :return: nothing
        """
        if self.log_text is not None:
            self.log_text.place_forget()
        self.log_text = tk.Text(self.window)
        with open("defense.log", "r") as f:
            log_contents = f.read()
        self.log_text.insert(tk.END, log_contents)
        self.log_text.place(x=300, y=140)

    def update_pc_listbox(self):
        """
        update the pc listbox.
        :return: nothing
        """
        i = 1
        for user_ip in self.db.get_all_users(self.A):
            user_ip = str(user_ip).replace(")", "")
            user_ip = str(user_ip).replace("(", "")
            user_ip = str(user_ip).replace(",", "")
            user_ip = str(user_ip).replace("'", "")
            self.pc_ips_listbox.insert(i, user_ip)
            i += 1

    def update_server_listbox(self):
        """
        update the server listbox.
        :return: nothing
        """
        self.server_ips_listbox.delete(0, "end")
        i = 1
        for user_ip in self.db.get_all_users(self.S):
            user_ip = str(user_ip).replace(")", "")
            user_ip = str(user_ip).replace("(", "")
            user_ip = str(user_ip).replace(",", "")
            user_ip = str(user_ip).replace("'", "")
            self.server_ips_listbox.insert(i, user_ip)
            i += 1

    def update_blacklist_listbox(self):
        """
        update the blacklist listbox.
        :return: nothing
        """
        self.blacklist_ips_listbox.delete(0, "end")
        i = 1
        for user_ip in self.db.get_all_users(self.B):
            user_ip = str(user_ip).replace(")", "")
            user_ip = str(user_ip).replace("(", "")
            user_ip = str(user_ip).replace(",", "")
            user_ip = str(user_ip).replace("'", "")
            self.blacklist_ips_listbox.insert(i, user_ip)
            i += 1

    def update_whitelist_listbox(self):
        """
        update the whitelist listbox.
        :return: nothing
        """
        self.whitelist_ips_listbox.delete(0, "end")
        i = 1
        for user_ip in self.db.get_all_users(self.W):
            user_ip = str(user_ip).replace(")", "")
            user_ip = str(user_ip).replace("(", "")
            user_ip = str(user_ip).replace(",", "")
            user_ip = str(user_ip).replace("'", "")
            self.whitelist_ips_listbox.insert(i, user_ip)
            i += 1

    def update_pc_table(self):
        """
        updates the pc table gui, and changes the label data when the function been called.
        :return:
        """
        self.pc_len_data = self.db.server_users_packets_count(self.A)
        self.pc_last_data = self.db.get_startdate(self.A)
        self.pc_last_packet_label.config(text=f"Last New Request:\n {self.pc_last_data}",
                                         font=self.largefont)
        self.pc_users_count_label.config(text=f"Total Requests:\n {self.pc_len_data}",
                                         font=self.largefont)

    def update_server_table(self):
        """
        updates the server table gui, and changes the label data when the function been called.
        :return:
        """
        self.server_len_data = self.db.server_users_packets_count(self.S)
        self.server_last_data = self.db.get_startdate(self.S)
        self.server_last_packet_label.config(text=f"Last New Request:\n {self.server_last_data}",
                                             font=self.largefont)
        self.server_users_packets_count_label.config(text=f"Total Requests:\n {self.server_len_data}",
                                                     font=self.largefont)

    def update_whitelist_table(self):
        """
        updates the whitelist table gui, and changes the label data when the function been called.
        :return:
        """
        self.whitelist_len_data = self.db.server_users_count(self.W)
        self.whitelist_last_data = self.db.get_startdate(self.W)
        self.whitelist_last_packet_label.config(text=f"Last New User:\n {self.whitelist_last_data}",
                                                font=self.largefont)
        self.whitelist_users_count_label.config(text=f"Total Users:\n {self.whitelist_len_data}",
                                                font=self.largefont)

    def update_blacklist_table(self):
        """
        updates the blacklist table gui, and changes the label data when the function been called.
        :return:
        """
        self.blacklist_len_data = self.db.server_users_count(self.B)
        self.blacklist_last_data = self.db.get_startdate(self.B)
        self.blacklist_last_packet_label.config(text=f"Last New Blocked User:\n {self.blacklist_last_data}",
                                                font=self.largefont)
        self.blacklist_users_count_label.config(text=f"Total Blocked Users:\n {self.blacklist_len_data}",
                                                font=self.largefont)

    def allow_unblocking(self):
        """
        a function to the unblocking button, when clicked if the button on 'off' it creates a daemon process for the
        function start the function and change the unblocking bool into true, if the button was on 'on' it kills the
        process and change the unblocking bool into false.
        :return: nothing
        """
        if not self.unblocking:
            self.unblocking_btn.config(text="On", activebackground="red")
            self.unblocking_function_process = multiprocessing.Process(target=self.unblocking_function, daemon=True)
            self.unblocking_function_process.start()
            self.unblocking = True
        else:
            self.unblocking_btn.config(text="Off", activebackground="green")
            self.unblocking_function_process.kill()

            self.unblocking = False

    def run_on_off(self):
        """
        a function to the run button, when clicked if the button on 'off' it creates a daemon process for the
        function start the function and change the is_on bool into true, if the button was on 'on' it kills the
        process and change the is_on bool into false.
        :return: nothing
        """
        if not self.is_on:
            self.run_btn.config(text="On", bg="green")
            # -> here is the: main()
            self.main_function_process = multiprocessing.Process(target=self.main_function, args=(
                self.port, self.ip, self.max_pc_packets, self.max_server_packets), daemon=True)
            self.main_function_process.start()
            self.is_on = True
        else:
            self.run_btn.config(text="Off", bg="red")
            self.main_function_process.kill()
            self.is_on = False

    def save_server_packets_rate(self):
        """
        checks the server packets rate if valid. if valid it saves and pops a small approval window, else id pops a
        small error window which says that the packets rate aren't valid.
        :return: nothing
        """
        max_server_packets = self.server_packets_rate_entry.get()
        if max_server_packets.isnumeric() and 10000 > int(max_server_packets) > 1500:
            threading.Thread(target=messagebox.showinfo,
                             args=(
                                 "Server Packets Rate Notifications!",
                                 "Server max packets rate has changed successfully!"),
                             daemon=True).start()
            self.max_server_packets = self.server_packets_rate_entry.get()
            if self.is_on:
                self.run_on_off()
                self.run_on_off()
        else:
            threading.Thread(target=messagebox.showerror,
                             args=("Server Packets Rate Notifications!", "The entered max packets rate is "
                                                                         "not valid, "
                                                                         "please enter a valid "
                                                                         "one."),
                             daemon=True).start()

    def save_pc_packets_rate(self):
        """
        checks the pc packets rate if valid. if valid it saves and pops a small approval window, else id pops a
        small error window which says that the packets rate aren't valid.
        :return: nothing
        """
        max_pc_packets = self.pc_packets_rate_entry.get()
        if max_pc_packets.isnumeric() and 100000 > int(max_pc_packets) > 15000:
            threading.Thread(target=messagebox.showinfo,
                             args=("PC Packets Rate Notifications!", "PC max packets rate has changed successfully!"),
                             daemon=True).start()
            self.max_pc_packets = self.pc_packets_rate_entry.get()
            if self.is_on:
                self.run_on_off()
                self.run_on_off()
        else:
            threading.Thread(target=messagebox.showerror,
                             args=("PC Packets Rate Notifications!", "The entered max packets rate is "
                                                                     "not valid, "
                                                                     "please enter a valid "
                                                                     "one."),
                             daemon=True).start()

    def save_server_port(self):
        """
        checks the server port if valid. if valid it saves and pops a small approval window, else id pops a
        small error window which says that the port aren't valid.
        :return: nothing
        """
        port: str = self.server_port_entry.get()
        if port.isnumeric() and 65530 > int(port) > 2500:
            threading.Thread(target=messagebox.showinfo,
                             args=("Server Port Notifications!", "Server port has changed successfully!"),
                             daemon=True).start()
            self.port = self.server_port_entry.get()
            if self.is_on:
                self.run_on_off()
                self.run_on_off()
        else:
            threading.Thread(target=messagebox.showerror, args=("Server port Notifications!", "The entered port is "
                                                                                              "not valid, "
                                                                                              "please enter a valid "
                                                                                              "one."),
                             daemon=True).start()

    def save_server_ip(self):
        """
        checks the server ip if valid. if valid it saves and pops a small approval window, else id pops a
        small error window which says that the ip aren't valid.
        :return: nothing
        """
        ip = self.server_ip_entry.get()
        if not (ip.count(".") != 3 or not all((i.isnumeric() and -1 < int(i) < 256 for i in ip.split(".")))):
            self.ip = self.server_ip_entry.get()
            threading.Thread(target=messagebox.showinfo, args=("Server IP Notifications!", "Server IP has changed "
                                                                                           "successfully!"),
                             daemon=True).start()

            if self.is_on:
                self.run_on_off()
                self.run_on_off()
        else:
            threading.Thread(target=messagebox.showerror, args=(
                "Server IP Notifications!", "The entered ip is not valid, please enter a valid one."),
                             daemon=True).start()

    def log_command(self):
        """
        the log command: that forgets all the menu frame widgets, and creates its own.
        :return: nothing
        """
        # forget all
        self.log_data_btn.place_forget()
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.back_to_menu_log_btn.pack(side="left")
        self.refresh_log_btn.pack(side="right")

    def menu_screen(self):
        """
        the command that shows all the menu frame widgets.
        :return: nothing
        """
        self.background_label.place(x=0, y=50, relwidth=1, relheight=1)
        self.label.pack()
        self.log_data_btn.place(x=900, y=70)
        self.menu_options_btn.place(x=20, y=70)
        self.run_btn.place(x=500, y=300)

    def settings_command(self):
        """
        the settings command: that forgets all the menu frame widgets, and creates its own.
        shows all the options you can change, like server port, ip and also the packets rate and the unblocking option.
        :return: nothing
        """
        # forget all
        self.log_data_btn.place_forget()
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.setting_label.pack()
        self.back_to_menu_settings_btn.pack(side="left")

        self.server_port_label.place(x=230, y=70)
        self.save_server_port_btn.place(x=400, y=130)
        self.server_port_entry.place(x=236, y=140)

        self.server_ip_label.place(x=230, y=220)
        self.save_server_ip_btn.place(x=400, y=280)
        self.server_ip_entry.place(x=236, y=290)

        self.max_packets_rate_pc_label.place(x=230, y=370)
        self.save_pc_packets_rate_btn.place(x=550, y=430)
        self.pc_packets_rate_entry.place(x=236, y=440)

        self.max_packets_rate_server_label.place(x=700, y=70)
        self.save_server_packets_rate_btn.place(x=1090, y=130)
        self.server_packets_rate_entry.place(x=700, y=140)

        self.allow_unblocking_label.place(x=750, y=410)
        self.unblocking_btn.place(x=820, y=470)

    def whitelist_command(self):
        """
        the whitelist command: that forgets all the menu frame widgets, and creates its own.
        shows all the ips in the WhiteList table, and the current amount allowed users in the system.
        :return: nothing
        """
        # forget all
        self.log_data_btn.place_forget()
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.whitelist_label.pack()
        self.update_whitelist_table()
        self.update_whitelist_listbox()
        self.whitelist_users_count_label.place(x=230, y=70)
        self.whitelist_last_packet_label.place(x=600, y=70)
        self.whitelist_ips_listbox.place(x=430, y=250)
        self.back_to_menu_whitelist_btn.pack(side="left")

    def blacklist_command(self):
        """
        the blacklist command: that forgets all the menu frame widgets, and creates its own.
        shows all the ips in the Blacklist table, and the current amount of blocked users.
        :return: nothing
        """
        # forget all
        self.log_data_btn.place_forget()
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.blacklist_label.pack()
        self.update_blacklist_table()
        self.update_blacklist_listbox()
        self.blacklist_users_count_label.place(x=230, y=70)
        self.blacklist_last_packet_label.place(x=700, y=70)
        self.blacklist_ips_listbox.place(x=430, y=250)
        self.back_to_menu_blacklist_btn.pack(side="left")

    def server_packets_command(self):
        """
        the server packets command: that forgets all the menu frame widgets, and creates its own.
        shows all the ips in the ServerRequests table, and the current amount of requests to the server.
        :return: nothing
        """
        # forget all
        self.log_data_btn.place_forget()
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.server_packets_label.pack()
        self.update_server_table()
        self.update_server_listbox()
        self.server_users_packets_count_label.place(x=230, y=70)
        self.server_last_packet_label.place(x=700, y=70)
        self.server_ips_listbox.place(x=430, y=250)
        self.back_to_menu_server_packets_btn.pack(side="left")

    def all_packets_command(self):
        """
        the all packets command or pc command: that forgets all the menu frame widgets, and creates its own.
        shows all the ips in the AllRequests table, and the current amount of requests to the pc.
        :return: nothing
        """
        # forget all
        self.log_data_btn.place_forget()
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.all_packets_label.pack()
        self.update_pc_table()
        self.update_pc_listbox()
        self.pc_users_count_label.place(x=230, y=70)
        self.pc_last_packet_label.place(x=700, y=70)
        self.pc_ips_listbox.place(x=430, y=250)
        self.back_to_menu_all_packets_btn.pack(side="left")

    def back_btn_from_settings(self):
        """
        the back button to the menu frame from the settings frame.
        :return: nothing
        """
        # forget all
        self.setting_label.pack_forget()
        self.background_label.place_forget()

        self.server_port_label.place_forget()
        self.save_server_port_btn.place_forget()
        self.server_port_entry.place_forget()

        self.server_ip_label.place_forget()
        self.save_server_ip_btn.place_forget()
        self.server_ip_entry.place_forget()

        self.max_packets_rate_pc_label.place_forget()
        self.save_pc_packets_rate_btn.place_forget()
        self.pc_packets_rate_entry.place_forget()

        self.max_packets_rate_server_label.place_forget()
        self.save_server_packets_rate_btn.place_forget()
        self.server_packets_rate_entry.place_forget()

        self.allow_unblocking_label.place_forget()
        self.unblocking_btn.place_forget()

        self.back_to_menu_settings_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_whitelist(self):
        """
        the back button to the menu frame from the whitelist frame.
        :return: nothing
        """
        # forget all
        self.whitelist_label.pack_forget()
        self.background_label.place_forget()
        self.whitelist_users_count_label.place_forget()
        self.whitelist_last_packet_label.place_forget()
        self.whitelist_ips_listbox.place_forget()
        self.back_to_menu_whitelist_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_blacklist(self):
        """
        the back button to the menu frame from the blacklist frame.
        :return: nothing
        """
        # forget all
        self.blacklist_label.pack_forget()
        self.background_label.place_forget()
        self.blacklist_users_count_label.place_forget()
        self.blacklist_last_packet_label.place_forget()
        self.blacklist_ips_listbox.place_forget()
        self.back_to_menu_blacklist_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_server_packets(self):
        """
        the back button to the menu frame from the server packets frame.
        :return: nothing
        """
        # forget all
        self.server_packets_label.pack_forget()
        self.background_label.place_forget()
        self.server_users_packets_count_label.place_forget()
        self.server_last_packet_label.place_forget()
        self.server_ips_listbox.place_forget()
        self.back_to_menu_server_packets_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_all_packets(self):
        """
        the back button to the menu frame from the all packets frame.
        :return: nothing
        """
        # forget all
        self.all_packets_label.pack_forget()
        self.background_label.place_forget()
        self.pc_users_count_label.place_forget()
        self.pc_last_packet_label.place_forget()
        self.pc_ips_listbox.place_forget()
        self.back_to_menu_all_packets_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_log(self):
        """
        the back button to the menu frame from the logging frame.
        :return: nothing
        """
        # forget all
        self.refresh_log_btn.pack_forget()
        self.log_text.place_forget()
        self.back_to_menu_log_btn.pack_forget()
        self.menu_screen()
