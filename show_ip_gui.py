import socket
import fcntl
import struct
import tkinter as tk
from tkinter import messagebox

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
        return ip_address
    except IOError:
        return None

def show_ip():
    eth_ip = get_ip_address('eth0')
    wlan_ip = get_ip_address('wlan0')

    if eth_ip:
        messagebox.showinfo("IP Address", f"Ethernet IP Address: {eth_ip}")
    elif wlan_ip:
        messagebox.showinfo("IP Address", f"Wi-Fi IP Address: {wlan_ip}")
    else:
        messagebox.showerror("Error", "Could not get IP address.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    show_ip()
    root.mainloop()
