import tkinter as tk
from black_client import Black_client


class FirewallApp:
    def __init__(self, root):
        self.root = root
        root.title("Firewall Application")

        self.label = tk.Label(root, text="Welcome to the Firewall Application")
        self.label.pack()

        self.ip_label = tk.Label(root, text="Enter IP address:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        # self.port_label = tk.Label(root, text="Enter port number:")
        # self.port_label.pack()

        # self.port_entry = tk.Entry(root)
        # self.port_entry.pack()

        self.block_button = tk.Button(root, text="Block", command=self.block)
        self.block_button.pack()

        self.unblock_button = tk.Button(root, text="Unblock", command=self.unblock)
        self.unblock_button.pack()

        self.list_blocked_ips_button = tk.Button(root, text="List blocked IP addresses", command=self.list_blocked_ips)
        self.list_blocked_ips_button.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack()

    def block(self):
        ip = self.ip_entry.get()

        if not ip:
            self.label.config(text="Please enter both an IP address and a port number.")
            return

        # Call the code to block an IP address and port here
        self.label.config(text=f"IP address {ip} blocked.")

    def unblock(self):
        ip = self.ip_entry.get()
        if not ip:
            self.label.config(text="Please enter both an IP address and a port number.")
            return

        # Call the code to unblock an IP address and port here
        self.label.config(text=f"IP address {ip} unblocked.")

    def list_blocked_ips(self, black_list: Black_client):
        # Call the code to retrieve a list of blocked IP addresses and ports here
        blocked_ips = black_list.get_all_ips()

        for ip in blocked_ips:
            self.listbox.insert(tk.END, ip)


if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallApp(root)
    root.mainloop()
