import tkinter as tk

LARGEFONT = ("Cascadia Code", 25)


class FirewallApp:
    def __init__(self, root):
        self.root = root
        root.title("Firewall Application")

        # load the image and resize it
        self.background_image = tk.PhotoImage(file="C:\\Users\\cyber\\Desktop\\pic.png")
        self.background_image = self.background_image.zoom(2)

        # set the background
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(root, text="Welcome to the Firewall Application", font=LARGEFONT, background="white")
        self.label.grid(row=1, column=2, padx=30, pady=10)

        self.block_button = tk.Button(root, text="\n\nBlack List\n\n", command=self.block, width=30)
        self.block_button.grid(column=1, row=143, padx=10, pady=400)

        self.unblock_button = tk.Button(root, text="\n\nSettings\n\n", command=self.show_settings, width=30)
        self.unblock_button.grid(column=2, row=143, padx=10, pady=400)

        self.white_list_button = tk.Button(root, text="\n\nWhite List\n\n", command=self.white_list, width=30)
        self.white_list_button.grid(column=3, row=143, padx=0, pady=400)

        # create a frame for the settings
        self.settings_frame = tk.Frame(root)

        # add some content to the settings frame
        settings_label = tk.Label(self.settings_frame, text="\n\nHere are the settings:\n\n", width=30)
        settings_label.pack()

        # add more widgets and content to the settings frame as desired
        # ...

    def block(self):
        pass

    def white_list(self):
        pass

    def show_settings(self):
        # hide the current frame
        self.label.grid_forget()
        self.block_button.grid_forget()
        self.unblock_button.grid_forget()
        self.white_list_button.grid_forget()

        # show the settings frame
        self.settings_frame.grid(row=1, column=2, padx=30, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallApp(root)
    root.minsize(1200, 700)
    root.maxsize(1200, 700)
    root.mainloop()
