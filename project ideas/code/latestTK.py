import tkinter as tk
from tkinter import messagebox

LARGEFONT = ("Cascadia Code", 25)


class FirewallApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Firewall Application")

        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.menu_frame = tk.Frame(container)
        self.menu_frame.grid(row=0, column=0, sticky="nwes")

        # load the image and resize it
        self.background_image = tk.PhotoImage(file="C:\\Users\\cyber\\Desktop\\pic.png")
        self.background_image = self.background_image.zoom(2)

        # set the background
        self.background_label = tk.Label(self.menu_frame, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self.menu_frame, text="Welcome to the Firewall Application", font=LARGEFONT)
        self.block_button = tk.Button(self.menu_frame, text="\n\nBlack List\n\n", command=self.show_blacklist, width=30)
        self.unblock_button = tk.Button(self.menu_frame, text="\n\nSettings\n\n", command=self.show_settings, width=30)
        # self.white_list_button = tk.Button(self.menu_frame, text="\n\nWhite List\n\n", command=self.show_whitelist, width=30)

        self.blocked_users = tk.Listbox(container, font=('Cascadia Code', 15))
        self.settings_frame = tk.Frame(container)
        self.settings_frame.grid(row=0, column=0, sticky="nwes")
        self.settings_label = tk.Label(self.settings_frame, text="Settings:", font=LARGEFONT)
        self.port_label = tk.Label(self.settings_frame, text="Enter Port Number:", font=('Cascadia Code', 20))
        self.port_entry = tk.Entry(self.settings_frame, font=('Cascadia Code', 20))
        self.save_button = tk.Button(self.settings_frame, text="Save", command=self.save_settings, width=30)
        self.back_button = tk.Button(self.settings_frame, text="Back to Menu", command=self.show_menu, width=30)

        self.show_menu()

    def show_menu(self):
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.grid(row=1, column=2)
        self.block_button.grid(column=1, row=2, pady=10)
        self.unblock_button.grid(column=2, row=2, pady=10)
        # self.white_list_button.grid(column=3, row=2, pady=10)
        self.menu_frame.tkraise()

    def show_blacklist(self):
        self.blocked_users.delete(0, tk.END)
        with open("blacklist.txt") as f:
            for line in f:
                self.blocked_users.insert(tk.END, line.strip())

        self.background_label.place_forget()
        self.blocked_users.grid(row=0, column=0, sticky="nwes")
        self.back_button_bl = tk.Button(self.blocked_users, text="Back to Menu", command=self.show_menu, width=30)
        self.back_button_bl.grid(column=0, row=1, padx=10, pady=10, sticky="e")
        self.blocked_users.tkraise()

    def show_settings(self):
        # hide the current frame
        self.label.grid_forget()
        self.block_button.grid_forget()
        self.unblock_button.grid_forget()
        # self.white_list_button.grid_forget()
        # show the settings frame
        self.settings_label.pack()
        self.back_button.pack()
        self.settings_frame.tkraise()

    def save_settings(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallApp(root)
    root.minsize(1200, 700)
    root.maxsize(1200, 700)
    root.mainloop()
