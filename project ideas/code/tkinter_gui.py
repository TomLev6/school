import tkinter as tk

LARGEFONT = ("Cascadia Code", 25)


class FirewallApp:
    def __init__(self, root):
        self.root = root
        root.title("Firewall Application")

        # load the image and resize it
        self.background_image = tk.PhotoImage(file="C:/Users/cyber/Desktop/pic.png")
        self.background_image = self.background_image.zoom(2)

        # set the background
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(root, text="Welcome to the Firewall Application", font=LARGEFONT, background="white")
        self.label.grid(row=1, column=2, padx=30,pady=10)

        self.block_button = tk.Button(root, text="\n\nBlack List\n\n", command=self.block, width=30)
        self.block_button.grid(column=1, row=143, padx=10, pady=400)

        self.unblock_button = tk.Button(root, text="\n\nSettings\n\n", command=self.unblock, width=30)
        self.unblock_button.grid(column=2, row=143, padx=10, pady=400)

        self.block_button = tk.Button(root, text="\n\nWhite List\n\n", command=self.block, width=30)
        self.block_button.grid(column=3, row=143, padx=0, pady=400)

    def block(self):
        pass

    def unblock(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallApp(root)
    root.minsize(1200, 700)
    root.maxsize(1200, 700)
    root.mainloop()
