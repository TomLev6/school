import tkinter as tk


# TODO: add the table stats to their section (the white list users to the whitelist section).
# TODO: make the on and off buttons start real functions

class Tk:
    def __init__(self, window: tk.Tk, main_function, unblocking_function):
        self.window = window
        self.main_function = main_function
        self.unblocking_function = unblocking_function
        self.window.title("Firewall Application")
        self.background_image = tk.PhotoImage(file="C:\\Users\\yonat\\PycharmProjects\\2.7\\d\\finalproject_ddos"
                                                   "\\backgr.png")
        self.largefont = ("Cascadia Code", 25)
        self.is_on = False
        self.unblocking = False
        self.port = "8909"
        self.ip = "192.168.1.13"

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

        # buttons
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

        self.save_server_port_btn = tk.Button(master=self.window, text=" > ", font=self.largefont, width=3,
                                              command=self.save_server_port)
        self.save_server_ip_btn = tk.Button(master=self.window, text=" > ", font=self.largefont, width=3,
                                            command=self.save_server_ip)

        # entries
        self.server_port_entry = tk.Entry(master=self.window, font=self.largefont, bd=3, fg="green", width=8)
        self.server_ip_entry = tk.Entry(master=self.window, font=self.largefont, bd=3, fg="green", width=8)

        # list box
        self.max_packets_rate_pc_listbox = tk.Listbox(master=self.window, bd=3, width=20, height=5, selectmode="single",
                                                      fg="green", font=self.largefont)
        self.max_packets_rate_pc_listbox.insert(1, 20000)
        self.max_packets_rate_pc_listbox.insert(2, 24000)
        self.max_packets_rate_pc_listbox.insert(3, 28000)
        self.max_packets_rate_pc_listbox.insert(4, 32000)
        self.max_packets_rate_pc_listbox.insert(5, 36000)

        self.max_packets_rate_server_listbox = tk.Listbox(master=self.window, bd=3, width=24, height=5,
                                                          selectmode="single", fg="green", font=self.largefont)
        self.max_packets_rate_server_listbox.insert(1, 8000)
        self.max_packets_rate_server_listbox.insert(2, 9000)
        self.max_packets_rate_server_listbox.insert(3, 10000)
        self.max_packets_rate_server_listbox.insert(4, 11000)
        self.max_packets_rate_server_listbox.insert(5, 12000)

        # menubutton
        self.menu_options_btn = tk.Menubutton(master=self.window, text="Options", relief="raised", font=self.largefont)
        self.menu_options_btn.menu = tk.Menu(self.menu_options_btn, tearoff=0)
        self.menu_options_btn["menu"] = self.menu_options_btn.menu
        self.menu_options_btn.menu.add_command(label="Settings", command=self.settings_command, font=self.largefont)
        self.menu_options_btn.menu.add_command(label="WhiteList", command=self.whitelist_command, font=self.largefont)
        self.menu_options_btn.menu.add_command(label="BlackList", command=self.blacklist_command, font=self.largefont)
        self.menu_options_btn.menu.add_command(label="ServerPackets", command=self.server_packets_command,
                                               font=self.largefont)
        self.menu_options_btn.menu.add_command(label="AllPackets", command=self.all_packets_command,
                                               font=self.largefont)

        self.menu_screen()

    # def whitelist_table(self):
    #     conn = db.conn_string.cursor()
    #     conn.execute("SELECT * FROM WhiteList;")
    #     i = 1
    #     for user in conn:
    #         e = tk.Entry(self.window, width=10, fg="green")
    #         e.place(x=20, y=i*20)
    #         e.insert()

    def allow_unblocking(self):
        if not self.unblocking:
            self.unblocking_btn.config(text="On", activebackground="red")
            # -> here is the: unblocking()
            self.unblocking_function()
            self.unblocking = True
        else:
            self.unblocking_btn.config(text="Off", activebackground="green")
            self.unblocking = False

    def run_on_off(self):
        if not self.is_on:
            self.run_btn.config(text="On", activebackground="red")
            # -> here is the: main()
            self.main_function()
            self.is_on = True
        else:
            self.run_btn.config(text="Off", activebackground="green")
            # self.main_function.exit()
            self.is_on = False

    def save_server_port(self):
        self.port = self.server_port_entry.get()

    def save_server_ip(self):
        self.ip = self.server_ip_entry.get()

    def menu_screen(self):
        self.background_label.place(x=0, y=50, relwidth=1, relheight=1)
        self.label.pack()

        self.menu_options_btn.place(x=20, y=70)
        self.run_btn.place(x=500, y=300)

    def settings_command(self):
        # forget all
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # self.whitelist_btn.pack_forget()
        # self.blacklist_btn.pack_forget()
        # self.server_packets_btn.pack_forget()
        # self.all_packets_btn.pack_forget()
        # self.optinos_btn.pack_forget()

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
        self.max_packets_rate_pc_listbox.place(x=230, y=420)

        self.max_packets_rate_server_label.place(x=700, y=70)
        self.max_packets_rate_server_listbox.place(x=700, y=120)

        self.allow_unblocking_label.place(x=750, y=410)
        self.unblocking_btn.place(x=820, y=470)

    def whitelist_command(self):
        # forget all
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.whitelist_label.pack()
        self.back_to_menu_whitelist_btn.pack(side="left")

    def blacklist_command(self):
        # forget all
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.blacklist_label.pack()
        self.back_to_menu_blacklist_btn.pack(side="left")

    def server_packets_command(self):
        # forget all
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.server_packets_label.pack()
        self.back_to_menu_server_packets_btn.pack(side="left")

    def all_packets_command(self):
        # forget all
        self.label.pack_forget()
        self.run_btn.place_forget()
        self.menu_options_btn.place_forget()

        # create new
        self.all_packets_label.pack()
        self.back_to_menu_all_packets_btn.pack(side="left")

    def back_btn_from_settings(self):
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
        self.max_packets_rate_pc_listbox.place_forget()

        self.max_packets_rate_server_label.place_forget()
        self.max_packets_rate_server_listbox.place_forget()

        self.allow_unblocking_label.place_forget()
        self.unblocking_btn.place_forget()

        self.back_to_menu_settings_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_whitelist(self):
        # forget all
        self.whitelist_label.pack_forget()
        self.background_label.place_forget()
        self.back_to_menu_whitelist_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_blacklist(self):
        # forget all
        self.blacklist_label.pack_forget()
        self.background_label.place_forget()
        self.back_to_menu_blacklist_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_server_packets(self):
        # forget all
        self.server_packets_label.pack_forget()
        self.background_label.place_forget()
        self.back_to_menu_server_packets_btn.pack_forget()
        self.menu_screen()

    def back_btn_from_all_packets(self):
        # forget all
        self.all_packets_label.pack_forget()
        self.background_label.place_forget()
        self.back_to_menu_all_packets_btn.pack_forget()
        self.menu_screen()

# last row
window = tk.Tk()
t = Tk(window, None, None)
window.minsize(1200, 700)
window.maxsize(1200, 700)
window.mainloop()
